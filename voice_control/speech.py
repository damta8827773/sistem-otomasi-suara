"""Spoken replies. Delegates to the cross-platform system_ops.speak and honors
the VOICE_SPEAK setting."""

from __future__ import annotations

from .config import CONFIG
from . import system_ops


def speak(text: str, lang: str | None = None) -> None:
    if not CONFIG.speak_replies or not text:
        return
    system_ops.speak(text)
