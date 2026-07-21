"""Entry point: `python -m voice_control`.

Listens continuously, transcribes each utterance in any language, runs the
matching action on the laptop, and speaks a short reply.
"""

from __future__ import annotations

import sys

from .actions import execute
from .config import CONFIG
from .intents import parse_intent
from .listener import Microphone
from .speech import speak
from .transcriber import Transcriber


def _use_utf8() -> None:
    # Windows consoles may default to a legacy code page; force UTF-8 so the
    # status glyphs and non-ASCII transcripts print correctly.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass


def main() -> None:
    _use_utf8()

    print("=== Sistem Otomasi Suara ===")
    print(f"Memuat model Whisper '{CONFIG.model_size}' (unduhan pertama bisa beberapa menit)...")
    transcriber = Transcriber()

    mic = Microphone()
    print("Siap. Ucapkan perintah Anda. Tekan Ctrl+C untuk berhenti.")
    print("Contoh: 'buka youtube', 'cari resep nasi goreng', 'jam berapa', 'kunci layar'.\n")

    try:
        for audio in mic.utterances():
            text, lang = transcriber.transcribe(audio)
            if not text:
                continue

            print(f"  ● didengar [{lang}]: {text}")
            intent = parse_intent(text)
            result = execute(intent, lang)
            mark = "✓" if result.ok else "✗"
            print(f"  {mark} {result.message}\n")

            speak(result.message, lang)
            if intent.action == "quit":
                break
    except KeyboardInterrupt:
        pass

    print("\nSistem dihentikan.")


if __name__ == "__main__":
    main()
