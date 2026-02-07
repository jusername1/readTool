import logging
import os
import tempfile

import keyboard
from dotenv import load_dotenv

from readaloud_tool.clipboard import try_read_selected_text
from readaloud_tool.player import AudioPlayer
from readaloud_tool.speaker import Speaker
from readaloud_tool.tts_openai import OpenAITts
from readaloud_tool.ui_status import StatusUi


def main() -> None:
    load_dotenv()

    log_path = os.path.join(tempfile.gettempdir(), "readaloud_tool.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info("Readaloud tool starting")

    speaker: Speaker | None = None

    def cleanup() -> None:
        if speaker is not None:
            speaker.stop()
        keyboard.unhook_all_hotkeys()
        ui.call_soon(ui.close)

    def stop() -> None:
        if speaker is None:
            return
        speaker.stop()

    def read_selection() -> None:
        try:
            ui.clear_error()
            ui.set_status("Reading selection...")
            logging.info("Read selection requested")
            text = try_read_selected_text(timeout_s=1.0)
            if not text:
                ui.set_status("Ready")
                ui.set_error("No text selected. Highlight text and try again.")
                return
            if speaker is None:
                ui.set_status("Ready")
                ui.set_error("TTS is not initialized.")
                return
            speaker.speak(text)
        except Exception as exc:
            logging.exception("Read selection failed")
            ui.set_error(f"Unexpected error: {exc}")

    def test_voice() -> None:
        try:
            ui.clear_error()
            logging.info("Test voice requested")
            if speaker is None:
                ui.set_error("TTS is not initialized.")
                return
            speaker.speak("This is a test of the read aloud tool.")
        except Exception as exc:
            logging.exception("Test voice failed")
            ui.set_error(f"Unexpected error: {exc}")

    ui = StatusUi(
        on_read_selection=read_selection,
        on_stop=stop,
        on_test_voice=test_voice,
        on_quit=cleanup,
        log_path=log_path,
    )

    try:
        tts = OpenAITts()
        player = AudioPlayer()
        speaker = Speaker(tts=tts, player=player, on_status=ui.set_status, on_error=ui.set_error)
        ui.set_status("Ready")
    except Exception as exc:
        logging.exception("Startup failed")
        ui.set_status("Not ready")
        ui.set_error(f"Startup error: {exc}")
        ui.set_actions_enabled(False)

    try:
        keyboard.add_hotkey("ctrl+alt+r", read_selection, suppress=False)
        keyboard.add_hotkey("ctrl+alt+s", stop, suppress=False)
        keyboard.add_hotkey("ctrl+alt+q", cleanup, suppress=False)
    except Exception as exc:
        logging.exception("Hotkey registration failed")
        ui.set_error(f"Hotkey registration failed: {exc}")

    ui.run()


if __name__ == "__main__":
    main()
