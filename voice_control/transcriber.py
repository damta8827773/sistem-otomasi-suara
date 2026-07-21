"""Speech to text with faster-whisper. The model auto-detects the spoken
language, so commands can be given in any language Whisper supports."""

from __future__ import annotations

import numpy as np
from faster_whisper import WhisperModel

from .config import CONFIG, Config


class Transcriber:
    def __init__(self, cfg: Config = CONFIG) -> None:
        self.cfg = cfg
        # The model is downloaded and cached on first use.
        self.model = WhisperModel(
            cfg.model_size, device=cfg.device, compute_type=cfg.compute_type
        )

    def transcribe(self, audio: np.ndarray) -> tuple[str, str]:
        """Return (text, detected_language_code)."""
        segments, info = self.model.transcribe(
            audio,
            language=self.cfg.language,
            beam_size=1,
            vad_filter=True,
        )
        text = "".join(segment.text for segment in segments).strip()
        return text, info.language
