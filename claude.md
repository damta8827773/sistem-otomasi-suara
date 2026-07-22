# Project: Sistem Otomasi Suara

A terminal voice controller for the laptop. You run `python -m voice_control`,
speak a command in any language, and the program performs the action on the real
operating system (open apps and sites, control volume, lock the screen). It
speaks a short reply back. Voice is the only input. There is no web UI.

> HISTORY (so the goal is not misread again): earlier attempts built (1) a
> native Rust/Go/C++ "voice OS", (2) a personal portfolio blog, and (3) a
> Next.js voice web app. All wrong. A web app runs inside a browser sandbox and
> cannot control the laptop. The real goal is THIS: a local terminal program
> that listens and drives the actual system.

## Stack

- **Language:** Python 3.10+ (tested on 3.14)
- **Speech to text:** faster-whisper (Whisper), auto-detects language, offline
  after the one-time model download
- **Microphone:** sounddevice (bundled PortAudio, no external binary)
- **Actions:** cross-platform, isolated in `system_ops.py` (Windows: shell +
  ctypes + SAPI; macOS: open/osascript/say/pmset; Linux: xdg-open/pactl/espeak)
- **Platform:** Windows (fully tested), macOS and Linux (best-effort)

## Data flow

```
mic -> listener (VAD) -> transcriber (Whisper) -> parse_intent -> execute -> speak
```

## Structure

```
voice_control/
  __main__.py     entry point and main loop
  config.py       settings via env vars (VOICE_MODEL, VOICE_LANG, ...)
  listener.py     mic capture + energy based voice activity detection
  transcriber.py  faster-whisper wrapper (language=None => auto)
  intents.py      keyword table -> Intent (multi language)
  actions.py      ActionResult execute(): platform-neutral command mapping
  system_ops.py   all OS-specific ops (open, volume, lock, speak) per platform
  speech.py       speak(): honors VOICE_SPEAK, delegates to system_ops
requirements.txt  faster-whisper, sounddevice, numpy
run.bat           launcher using the .venv
```

## Conventions

- **Voice only, terminal only.** No web server, no GUI, no dashboard.
- **Adding a command** is two edits: keywords in `intents.py` and a branch in
  `actions.py`.
- **Actions must be real system actions** (this is the whole point) and are
  Windows specific for now.
- Keep the model default at `base`; `small` is the fallback for better accuracy.

## Commands

```sh
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m voice_control      # run (or double-click run.bat)
```

Environment: `VOICE_MODEL` (tiny|base|small|medium), `VOICE_LANG` (empty=auto),
`VOICE_THRESHOLD` (mic sensitivity), `VOICE_SPEAK` (0 to mute replies).

Note: the working directory is `sistem otomatis`. The separate real personal
site lives at `C:\Users\ASUS\Desktop\damtaweb.com` and must not be touched.
Bun is not installed here.
