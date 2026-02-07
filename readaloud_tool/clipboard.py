import time
from typing import Optional

import keyboard
import win32clipboard
import win32con


def _get_clipboard_text() -> Optional[str]:
    try:
        win32clipboard.OpenClipboard()
        try:
            if not win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                return None
            return win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        return None


def _set_clipboard_text(text: str) -> None:
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    finally:
        win32clipboard.CloseClipboard()


def _clipboard_sequence_number() -> int:
    # GetClipboardSequenceNumber is in user32.
    import ctypes

    return int(ctypes.windll.user32.GetClipboardSequenceNumber())


def try_read_selected_text(timeout_s: float = 1.0) -> Optional[str]:
    """Try to read currently selected text by sending Ctrl+C.

    Best-effort restores previous *text* clipboard contents.
    """

    prev_text = _get_clipboard_text()
    seq0 = _clipboard_sequence_number()

    # Trigger copy.
    keyboard.press_and_release("ctrl+c")

    # Wait for clipboard to update.
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _clipboard_sequence_number() != seq0:
            break
        time.sleep(0.02)

    copied = _get_clipboard_text()

    # Restore previous text clipboard content.
    if prev_text is not None:
        try:
            _set_clipboard_text(prev_text)
        except Exception:
            pass

    if copied is None:
        return None

    copied = copied.strip()
    return copied if copied else None
