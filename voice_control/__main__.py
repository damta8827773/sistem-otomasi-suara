"""Entry point: `python -m voice_control`.

Listens continuously, transcribes each utterance, runs the matching action on
the laptop, and speaks a short reply. The loop is defensive: one failed command
never stops the system.
"""

from __future__ import annotations

import re
import sys

from . import system_ops
from .actions import execute
from .config import CONFIG
from .intents import is_probably_noise, parse_intent
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


def main() -> int:
    _use_utf8()

    print("=== Sistem Otomasi Suara ===")
    print(f"Sistem operasi: {system_ops.OS_NAME}")
    print(f"Memuat model Whisper '{CONFIG.model_size}' (unduhan pertama bisa beberapa menit)...")

    try:
        transcriber = Transcriber()
    except Exception as exc:
        print(f"Gagal memuat model Whisper: {exc}")
        print("Pastikan ada koneksi internet untuk unduhan pertama, lalu coba lagi.")
        return 1

    mic = Microphone()
    print("Siap. Ucapkan perintah Anda. Tekan Ctrl+C untuk berhenti.")
    print("Contoh: 'buka youtube', 'cari resep nasi goreng', 'jam berapa', 'kunci layar'.\n")

    try:
        for audio in mic.utterances():
            try:
                text, lang = transcriber.transcribe(audio)
            except Exception as exc:
                print(f"  ! gagal mengenali suara: {exc}")
                continue

            # Drop empty results, symbol-only output, and the stock phrases
            # Whisper invents from music or background noise.
            if not text or not re.search(r"\w", text, re.UNICODE):
                continue
            if is_probably_noise(text):
                continue

            print(f"  ● didengar [{lang}]: {text}")
            intent = parse_intent(text)

            try:
                result = execute(intent, lang)
            except Exception as exc:
                print(f"  ! gagal menjalankan perintah: {exc}\n")
                continue

            mark = "✓" if result.ok else "✗"
            print(f"  {mark} {result.message}\n")
            speak(result.message, lang)
            # Throw away whatever the mic picked up while we were talking.
            mic.drain()

            if intent.action == "quit":
                break
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"\nKesalahan audio/mikrofon: {exc}")
        print("Pastikan mikrofon tersedia dan tidak dipakai aplikasi lain.")
        return 1

    print("\nSistem dihentikan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
