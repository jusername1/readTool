import logging
import os
import time

import pygame


class AudioPlayer:
    def __init__(self) -> None:
        self._initialized = False
        self._current_path: str | None = None

    def _ensure_initialized(self) -> None:
        """Lazy-initialize pygame mixer to keep startup fast."""
        if self._initialized:
            return
        try:
            # Initialize just the mixer module (lighter than full pygame.init())
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._initialized = True
            logging.info("pygame.mixer initialized")
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize pygame.mixer: {exc}") from exc

    def play_wav_file_blocking(self, wav_path: str) -> None:
        """Play a WAV file and block until playback completes."""
        self._ensure_initialized()
        self._current_path = wav_path
        try:
            if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
                raise RuntimeError("Synthesized audio file is missing or empty")
            size_bytes = os.path.getsize(wav_path)
            logging.info("Playing WAV (%s bytes)", size_bytes)

            # Load and play the audio file
            pygame.mixer.music.load(wav_path)
            pygame.mixer.music.play()

            # Block until playback finishes (or is stopped externally)
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

        finally:
            self._current_path = None
            # Best-effort cleanup of temp files
            try:
                os.remove(wav_path)
            except OSError:
                pass

    def stop(self) -> None:
        """Stop any currently playing audio immediately."""
        if not self._initialized:
            return
        pygame.mixer.music.stop()
