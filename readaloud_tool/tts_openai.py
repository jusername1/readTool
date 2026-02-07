import os
import tempfile
import time

from openai import OpenAI


class OpenAITts:
    def __init__(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=api_key)

        self.model = "gpt-4o-mini-tts"
        self.voice = os.environ.get("OPENAI_TTS_VOICE", "cedar")
        self.instructions = (
            "Read clearly and naturally. "
            "Use a warm, calm tone. "
            "Pause slightly after sentences. "
            "Do not spell out punctuation."
        )

    def synthesize_to_wav_file(self, text: str) -> str:
        ts = int(time.time() * 1000)
        out_path = os.path.join(tempfile.gettempdir(), f"readaloud_{ts}.wav")

        with self._client.audio.speech.with_streaming_response.create(
            model=self.model,
            voice=self.voice,
            input=text,
            instructions=self.instructions,
            response_format="wav",
        ) as resp:
            resp.stream_to_file(out_path)

        return out_path
