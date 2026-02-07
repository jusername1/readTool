import logging
import os
import ctypes
import winsound


class AudioPlayer:
    def __init__(self) -> None:
        self._current_path: str | None = None

    def play_wav_file_blocking(self, wav_path: str) -> None:
        self._current_path = wav_path
        try:
            if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
                raise RuntimeError("Synthesized audio file is missing or empty")
            size_bytes = os.path.getsize(wav_path)
            logging.info("Playing WAV (%s bytes)", size_bytes)
            # Blocking playback so we can chain chunks in order.
            flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT
            try:
                ok = winsound.PlaySound(wav_path, flags)
            except RuntimeError:
                ok = False
            if ok is False:
                logging.warning("winsound.PlaySound failed, trying MCI")
                try:
                    self._play_with_mci(wav_path)
                    return
                except Exception:
                    logging.exception("MCI playback failed")
                    self._play_with_simpleaudio(wav_path)
        finally:
            self._current_path = None
            # Best-effort cleanup of temp files.
            try:
                os.remove(wav_path)
            except OSError:
                pass

    def stop(self) -> None:
        winsound.PlaySound(None, winsound.SND_PURGE)

    def _play_with_mci(self, wav_path: str) -> None:
        alias = "readaloud"
        open_cmd = f'open "{wav_path}" type waveaudio alias {alias}'
        self._mci_send(open_cmd)
        try:
            self._mci_send(f"play {alias} wait")
        finally:
            self._mci_send(f"close {alias}")

    @staticmethod
    def _mci_send(command: str) -> None:
        buf = ctypes.create_unicode_buffer(256)
        winmm = ctypes.windll.winmm
        code = winmm.mciSendStringW(command, buf, len(buf), 0)
        if code != 0:
            err_buf = ctypes.create_unicode_buffer(256)
            winmm.mciGetErrorStringW(code, err_buf, len(err_buf))
            message = err_buf.value or f"MCI error {code}"
            raise RuntimeError(message)

    @staticmethod
    def _play_with_simpleaudio(wav_path: str) -> None:
        try:
            import simpleaudio
        except Exception as exc:
            raise RuntimeError(f"simpleaudio is not available: {exc}") from exc

        try:
            wave_obj = simpleaudio.WaveObject.from_wave_file(wav_path)
        except Exception as exc:
            raise RuntimeError(f"simpleaudio failed to load wav: {exc}") from exc

        play_obj = wave_obj.play()
        play_obj.wait_done()
