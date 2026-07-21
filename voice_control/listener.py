"""Microphone capture with a small energy based voice activity detector.

The stream runs continuously. Audio is buffered while you speak and flushed as
one utterance once a short silence follows, so the system is hands free.
"""

from __future__ import annotations

import queue
from typing import Iterator

import numpy as np
import sounddevice as sd

from .config import CONFIG, Config


class Microphone:
    def __init__(self, cfg: Config = CONFIG) -> None:
        self.cfg = cfg
        self.frame_len = int(cfg.sample_rate * cfg.frame_ms / 1000)
        self._q: "queue.Queue[np.ndarray]" = queue.Queue()

    def _callback(self, indata, frames, time_info, status) -> None:  # noqa: ANN001
        # indata is float32 with shape (frames, 1); keep a copy of channel 0.
        self._q.put(indata[:, 0].copy())

    def _calibrate(self, seconds: float = 0.5) -> float:
        """Measure the ambient noise floor and derive a speech threshold."""
        samples = []
        for _ in range(int(seconds * 1000 / self.cfg.frame_ms)):
            frame = self._q.get()
            samples.append(float(np.sqrt(np.mean(frame**2))))
        floor = float(np.mean(samples)) if samples else 0.0
        return max(self.cfg.energy_threshold, floor * 3.5)

    def utterances(self) -> Iterator[np.ndarray]:
        cfg = self.cfg
        silence_frames = int(cfg.silence_ms / cfg.frame_ms)
        min_frames = int(cfg.min_speech_ms / cfg.frame_ms)

        with sd.InputStream(
            samplerate=cfg.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.frame_len,
            callback=self._callback,
        ):
            threshold = self._calibrate()

            collecting = False
            buffer: list[np.ndarray] = []
            silence_run = 0

            while True:
                frame = self._q.get()
                rms = float(np.sqrt(np.mean(frame**2)))
                speaking = rms >= threshold

                if speaking:
                    if not collecting:
                        collecting = True
                        buffer = []
                    buffer.append(frame)
                    silence_run = 0
                elif collecting:
                    buffer.append(frame)
                    silence_run += 1
                    if silence_run >= silence_frames:
                        collecting = False
                        speech_frames = len(buffer) - silence_run
                        if speech_frames >= min_frames:
                            yield np.concatenate(buffer)
                        buffer = []
                        silence_run = 0
