# Read Selected Text Aloud

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A lightweight Windows tool that reads selected text aloud using OpenAI Text-to-Speech. Press a hotkey to hear any text you've selected in any application.

## Features

- **Global hotkeys** for reading selected text anywhere on Windows
- **Smart clipboard handling** that copies your selection and restores previous clipboard content
- **High-quality speech** using OpenAI's TTS API (`gpt-4o-mini-tts` model)
- **Background playback** with instant stop functionality
- **Minimal and responsive** - no heavy dependencies or UI overhead

## Prerequisites

- **Python 3.10 or higher**
- **Windows OS** (uses Windows-specific clipboard APIs)
- **OpenAI API key** with TTS access

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/readTool.git
cd readTool
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

4. **Configure your API key**

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
copy .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_TTS_VOICE=cedar
```

Available voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`, `cedar`

## Usage

1. **Start the application**

```bash
python main.py
```

A small status window will appear. Keep it running in the background.

2. **Use hotkeys to control the tool**

| Hotkey | Action |
|--------|--------|
| `Ctrl+Alt+R` | Read selected text (copies selection via clipboard) |
| `Ctrl+Alt+S` | Stop speaking |
| `Ctrl+Alt+Q` | Quit application |

3. **Read text anywhere**
   - Select any text in any application
   - Press `Ctrl+Alt+R`
   - The tool will copy the selection, speak it, and restore your previous clipboard

## Troubleshooting

### Hotkeys not working
- The `keyboard` library sometimes requires elevated privileges on Windows
- Try running the script as Administrator
- Check that the hotkey combinations aren't already in use by another application

### Some applications don't allow text selection
- Some apps block programmatic clipboard access
- Try copying the text manually (`Ctrl+C`) then pressing the read hotkey

### Clipboard not restoring properly
- The tool only restores text clipboard contents
- If your clipboard contained images or files, they may not restore perfectly
- This is a limitation of Windows clipboard APIs

### API errors
- Verify your `OPENAI_API_KEY` is set correctly in `.env`
- Ensure you have TTS API access enabled on your OpenAI account
- Check the log file at `%TEMP%\readaloud_tool.log` for detailed error messages

## How It Works

1. **Hotkey trigger**: Global hotkey registered via the `keyboard` library
2. **Selection capture**: Simulates `Ctrl+C` to copy selected text
3. **Clipboard management**: Saves previous clipboard, extracts text, restores clipboard
4. **TTS synthesis**: Sends text to OpenAI TTS API, streams response to temp WAV file
5. **Audio playback**: Plays WAV file using `simpleaudio` in background thread
6. **Cleanup**: Deletes temp file after playback completes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

See [AGENTS.md](AGENTS.md) for development guidelines and coding conventions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [OpenAI Text-to-Speech API](https://platform.openai.com/docs/guides/text-to-speech)
- Uses the excellent `keyboard` library for global hotkeys
- Inspired by accessibility tools and text-to-speech utilities
