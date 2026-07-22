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

    def drain(self) -> None:
        """Discard buffered audio.

        Called after the system speaks so its own voice, and any media playing
        through the speakers meanwhile, is not transcribed as a command.
        """
        try:
            while True:
                self._q.get_nowait()
        except queue.Empty:
            pass

    def _calibrate(self, seconds: float = 0.5) -> float:
        """Measure the ambient noise floor."""
        samples = []
        for _ in range(int(seconds * 1000 / self.cfg.frame_ms)):
            frame = self._q.get()
            samples.append(float(np.sqrt(np.mean(frame**2))))
        return float(np.mean(samples)) if samples else 0.0

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
            # Noise floor adapts continuously, so speech is still detected when
            # music or a video starts playing through the speakers.
            noise = self._calibrate()

            collecting = False
            buffer: list[np.ndarray] = []
            silence_run = 0

            while True:
                frame = self._q.get()
                rms = float(np.sqrt(np.mean(frame**2)))

                if not collecting:
                    # Track the background level only between utterances.
                    noise = 0.95 * noise + 0.05 * rms

                threshold = max(cfg.energy_threshold, noise * 3.5)
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
