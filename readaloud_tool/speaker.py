import logging
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from readaloud_tool.player import AudioPlayer
from readaloud_tool.text import clean_text, chunk_text
from readaloud_tool.tts_openai import OpenAITts


class Speaker:
    def __init__(
        self,
        tts: OpenAITts,
        player: AudioPlayer,
        on_status: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        self._tts = tts
        self._player = player
        self._on_status = on_status
        self._on_error = on_error

        self._lock = threading.Lock()
        self._job_id = 0
        self._thread: threading.Thread | None = None

    def stop(self) -> None:
        with self._lock:
            self._job_id += 1
        self._player.stop()
        self._emit_status("Stopped")

    def speak(self, text: str) -> None:
        text = clean_text(text)
        if not text.strip():
            return

        with self._lock:
            self._job_id += 1
            job_id = self._job_id

        self._player.stop()
        self._emit_status("Speaking...")

        t = threading.Thread(target=self._run_job, args=(job_id, text), daemon=True)
        with self._lock:
            self._thread = t
        t.start()

    def _run_job(self, job_id: int, text: str) -> None:
        # Convert to list to enable lookahead
        chunks = list(chunk_text(text, max_chars=900))
        if not chunks:
            self._emit_status("Ready")
            return

        executor = ThreadPoolExecutor(max_workers=1)
        try:
            # Synthesize first chunk
            with self._lock:
                if job_id != self._job_id:
                    return

            try:
                current_wav = self._tts.synthesize_to_wav_file(chunks[0])
            except Exception as exc:
                logging.exception("TTS synthesis failed")
                self._emit_error(f"TTS failed: {self._format_error(exc)}")
                return

            # Process each chunk with lookahead
            for i in range(len(chunks)):
                # Check if cancelled
                with self._lock:
                    if job_id != self._job_id:
                        return

                # Start synthesizing next chunk in background (if exists)
                next_future = None
                if i + 1 < len(chunks):
                    next_future = executor.submit(
                        self._tts.synthesize_to_wav_file,
                        chunks[i + 1]
                    )

                # Play current chunk (blocking)
                try:
                    self._player.play_wav_file_blocking(current_wav)
                except Exception as exc:
                    logging.exception("Audio playback failed")
                    self._emit_error(f"Audio playback failed: {self._format_error(exc)}")
                    return

                # Wait for next synthesis to complete
                if next_future:
                    with self._lock:
                        if job_id != self._job_id:
                            return
                    try:
                        current_wav = next_future.result()
                    except Exception as exc:
                        logging.exception("TTS synthesis failed")
                        self._emit_error(f"TTS failed: {self._format_error(exc)}")
                        return
        finally:
            executor.shutdown(wait=False)
            with self._lock:
                should_emit = job_id == self._job_id
            if should_emit:
                self._emit_status("Ready")

    def _emit_status(self, message: str) -> None:
        if self._on_status is not None:
            self._on_status(message)

    def _emit_error(self, message: str) -> None:
        logging.error(message)
        if self._on_error is not None:
            self._on_error(message)

    @staticmethod
    def _format_error(exc: Exception) -> str:
        detail = str(exc).strip()
        return detail if detail else exc.__class__.__name__
