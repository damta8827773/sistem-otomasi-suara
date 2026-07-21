"""Runtime configuration. Everything can be overridden with environment
variables so the program can be tuned without editing code."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    # Whisper model size: tiny | base | small | medium. Bigger is more accurate
    # but slower and a larger download. "base" is a good balance on a laptop.
    model_size: str = os.getenv("VOICE_MODEL", "base")
    device: str = os.getenv("VOICE_DEVICE", "cpu")
    compute_type: str = os.getenv("VOICE_COMPUTE", "int8")

    # None means auto-detect the spoken language (works for any language).
    language: str | None = os.getenv("VOICE_LANG") or None

    # Audio capture.
    sample_rate: int = 16000
    frame_ms: int = 30

    # Utterance segmentation (simple energy based voice activity detection).
    silence_ms: int = 700          # trailing silence that ends an utterance
    min_speech_ms: int = 300       # ignore blips shorter than this
    energy_threshold: float = float(os.getenv("VOICE_THRESHOLD", "0.012"))

    # Speak the reply out loud (uses the Windows SAPI voice).
    speak_replies: bool = os.getenv("VOICE_SPEAK", "1") != "0"


CONFIG = Config()
