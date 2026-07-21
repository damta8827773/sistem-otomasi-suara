"""Spoken replies using the built-in Windows SAPI voice via PowerShell, so no
extra dependency is required."""

from __future__ import annotations

import subprocess

from .config import CONFIG


def speak(text: str, lang: str | None = None) -> None:
    if not CONFIG.speak_replies or not text:
        return

    safe = text.replace("'", "''")
    script = (
        "Add-Type -AssemblyName System.Speech;"
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        f"$s.Speak('{safe}')"
    )
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            timeout=15,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        # Speaking is best effort; never let it crash the loop.
        pass
