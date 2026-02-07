# Agent Notes (Repo Guide)

This repository is a small Windows-only Python tool that reads selected text aloud using
OpenAI Text-to-Speech. Keep changes minimal, keep the tool responsive, and avoid
introducing heavyweight dependencies.

## Project Layout
- `main.py`: entrypoint; registers global hotkeys and wires dependencies.
- `readaloud_tool/`: implementation modules (clipboard, OCR, text cleaning, TTS, audio).
- `requirements.txt`: runtime dependencies.
- `.env.example`: env var template (copy to `.env` locally).

## Cursor / Copilot Rules
No Cursor rules found in `.cursor/rules/` or `.cursorrules`.
No Copilot instructions found in `.github/copilot-instructions.md`.

## Setup / Build (Python)
There is no build system; install dependencies and run the script.
From repo root (PowerShell or cmd):

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Environment variables:
- `OPENAI_API_KEY`: required; set in `.env` (copy from `.env.example`).

Run:
```bash
python main.py
```

Notes: Windows-only; global hotkeys via `keyboard` sometimes require elevated privileges.

## Quick Sanity Checks

These avoid hotkeys/UI and are safe to run in CI or headless shells:

```bash
python -c "from readaloud_tool.text import clean_text, chunk_text; print(clean_text('Hello\\nworld')); print(list(chunk_text('A. B. C.', 3)))"
python -c "from readaloud_tool.tts_openai import OpenAITts; tts=OpenAITts(); print(tts.model, tts.voice)"
```

## Lint / Format / Typecheck
No linters/formatters/type checkers are configured in this repo today. If you add tooling,
prefer low-config defaults:

- Format: `ruff format` (or `black`).
- Lint: `ruff`.
- Types: `mypy` (optional; keep it pragmatic).

```bash
python -m ruff check .
python -m ruff format .
python -m mypy .
```

## Tests
There is no `tests/` directory currently.
If you add tests, prefer `pytest` and keep Windows-specific integration tests optional/guarded.
Suggested commands (once `pytest` is added):

```bash
python -m pytest
```

Run a single test (pytest):

```bash
# by file
python -m pytest tests/test_text.py

# by test node id
python -m pytest tests/test_text.py::test_clean_text

# by keyword expression
python -m pytest -k clean_text
```

## Coding Style (Repository Conventions)

### Imports
- Group imports in this order with a blank line between groups:
  1) stdlib
  2) third-party
  3) local (`readaloud_tool.*`)
- Prefer explicit imports over `import *`.
- Avoid heavy imports at module import time when they slow startup; lazy-import
  platform-specific APIs inside functions (example: `readaloud_tool/ocr.py`).

### Formatting
- Use 4 spaces; no tabs.
- Keep lines reasonably short (aim ~88-100 chars).
- Prefer early returns for guard clauses.
- Keep functions small and single-purpose; push platform glue into helpers.

### Types
- Python 3.10+ (this codebase uses `T | None`).
- Add type hints for public functions/methods and key helpers.
- Prefer built-in generics: `list[str]`, `dict[str, str]`, `tuple[int, ...]`.
- Prefer `T | None` over `Optional[T]` in new code (unless matching nearby style).

### Naming
- Modules/functions/vars: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Private helpers: prefix `_`.

### Error Handling
- Raise explicit, actionable errors for required configuration.
  Example: `readaloud_tool/tts_openai.py` raises `RuntimeError` if `OPENAI_API_KEY` is missing.
- For best-effort OS integrations (clipboard/OCR), returning `None` on failure is acceptable.
- Avoid bare `except:`; catch `Exception` only when intentionally degrading.
- Keep `except` blocks small; avoid catching exceptions that indicate programmer bugs.

Output: avoid printing clipboard contents or OCR text; keep `main.py` output minimal.

### Concurrency / Responsiveness
- Hotkey callbacks must be fast; do not do network calls on the main/hotkey thread.
- Preserve `readaloud_tool/speaker.py` behavior: background thread + job id cancellation.
- If adding additional background work, ensure `Speaker.stop()` reliably cancels playback.

### OpenAI TTS Usage
- OpenAI client wiring lives in `readaloud_tool/tts_openai.py`.
- Keep secrets out of logs and source control.
- If changing model/voice/instructions, prefer env-var configuration without breaking defaults.
- Keep synthesis streaming (`with_streaming_response`) so large text remains responsive.

### Filesystem / Temp Files
- `OpenAITts.synthesize_to_wav_file()` writes to `%TEMP%`.
- `readaloud_tool/player.py` deletes temp WAV files after playback (best effort).
- If you introduce new temp files, ensure cleanup even on error/stop.

### Windows-Specific Boundaries
- Keep Windows-only dependencies isolated to the smallest surface area.
- Gate any cross-platform behavior carefully; Windows must remain the primary target.
- Prefer lazy imports for WinRT/ctypes APIs to keep startup fast.

## Security / Hygiene
- Never commit secrets (API keys). `.env` is intentionally ignored by `.gitignore`.
- Keep `.env.example` updated when adding new env vars.
