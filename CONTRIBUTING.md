# Contributing to Read Selected Text Aloud

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository and clone your fork
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your OpenAI API key

## Code Style

This project follows standard Python conventions:

### Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line length**: Aim for ~88-100 characters
- **Imports**: Group in order (stdlib, third-party, local) with blank lines between
- **Functions**: Keep small and single-purpose

### Type Hints
- Python 3.10+ syntax (`str | None` instead of `Optional[str]`)
- Add type hints for public functions and key helpers
- Use built-in generics: `list[str]`, `dict[str, Any]`

### Naming
- Modules/functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private helpers: prefix with `_`

### Error Handling
- Raise explicit, actionable errors for configuration issues
- Avoid bare `except:` clauses
- For OS integrations (clipboard), returning `None` on failure is acceptable
- Keep `except` blocks focused and small

## Testing

Currently, there are no automated tests. When adding tests:

1. Use `pytest` as the testing framework
2. Place tests in a `tests/` directory
3. Keep Windows-specific integration tests optional/guarded
4. Run tests with: `python -m pytest`

## Quick Sanity Checks

These commands test core functionality without hotkeys:

```bash
# Test text processing
python -c "from readaloud_tool.text import clean_text, chunk_text; print(clean_text('Hello\nworld'))"

# Test TTS initialization
python -c "from readaloud_tool.tts_openai import OpenAITts; tts=OpenAITts(); print(tts.model, tts.voice)"
```

## Coding Guidelines

### Keep It Lightweight
- Avoid heavyweight dependencies
- Lazy-import platform-specific APIs when possible
- Keep startup time fast

### Windows-First
- This is a Windows-only tool using Windows-specific APIs
- Keep Windows dependencies isolated to specific modules
- Document any Windows version requirements

### Responsiveness
- Hotkey callbacks must be fast
- Never do network calls on the hotkey thread
- Use background threads for TTS synthesis and playback
- Ensure `Speaker.stop()` reliably cancels playback

### Security
- Never commit secrets (API keys)
- Keep `.env` in `.gitignore`
- Update `.env.example` when adding new environment variables
- Don't log clipboard contents or user text

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the code style above
3. **Test your changes** - ensure the tool still works correctly
4. **Update documentation** - modify README.md if adding features
5. **Submit a PR** with a clear description of changes

### PR Guidelines
- Keep PRs focused on a single feature or fix
- Write clear commit messages describing what and why
- Reference any related issues
- Be responsive to feedback and requested changes

## Project Structure

```
readTool/
├── main.py                  # Entry point, hotkey registration
├── readaloud_tool/          # Implementation modules
│   ├── clipboard.py         # Clipboard operations
│   ├── text.py              # Text cleaning/chunking
│   ├── tts_openai.py        # OpenAI TTS integration
│   ├── player.py            # Audio playback
│   ├── speaker.py           # Speech coordination
│   └── ui_status.py         # Status window UI
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── AGENTS.md                # Detailed development guide
└── README.md                # User documentation
```

## Reporting Issues

When reporting bugs, please include:

1. **Python version** (`python --version`)
2. **Windows version**
3. **Steps to reproduce** the issue
4. **Expected behavior** vs. actual behavior
5. **Log output** from `%TEMP%\readaloud_tool.log`

## Feature Requests

Feature requests are welcome! Please:

1. Check if the feature has already been requested
2. Describe the use case and benefits
3. Consider if it fits the "lightweight Windows tool" philosophy
4. Be open to discussion about implementation

## Questions?

Feel free to open an issue for questions or clarifications about contributing.

## Code of Conduct

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Maintain a positive and inclusive environment

Thank you for contributing!
