<div align="center">

# Sistem Otomasi Suara

A terminal voice controller for your laptop. Run it, speak, and your computer
acts. Say "buka youtube" and YouTube opens. Say "kunci layar" and the screen
locks. It understands any language, because it transcribes with Whisper.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Whisper](https://img.shields.io/badge/STT-faster--whisper-5A45FF)](https://github.com/SYSTRAN/faster-whisper)
[![Platform](https://img.shields.io/badge/Platform-Windows_%7C_macOS_%7C_Linux-0078D6)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

## What it does

This is not a website. It is a program you start from the terminal. It listens
to your microphone continuously, understands what you said in any language, and
runs the matching action on the real system.

```
microphone  ->  Whisper (any language)  ->  match command  ->  run on the laptop  ->  spoken reply
 (your voice)     faster-whisper              intents.py         actions.py            SAPI voice
```

## Commands

Speak naturally in Indonesian, English, or another language. Examples:

| Say                          | It does                              |
| :--------------------------- | :----------------------------------- |
| `buka youtube` / `open youtube` | Open a site or an installed app    |
| `cari resep nasi goreng`     | Search the web                       |
| `jam berapa` / `what time`   | Speak the current time               |
| `tanggal berapa`             | Speak today's date                   |
| `klik` / `buka ini` / `buka yang ditunjuk kursor` | Click whatever the mouse points at |
| `klik kanan` / `klik dua kali` | Right click / double click         |
| `sedang buka apa` / `baca layar` | Say which window is in focus      |
| `daftar jendela` / `list windows`| Say which windows are open        |
| `volume naik` / `volume down`| Change the system volume             |
| `bisukan` / `mute`           | Mute the sound                       |
| `kunci layar` / `lock screen`| Lock the workstation                 |
| `bantuan` / `help`           | List commands out loud               |
| `berhenti` / `stop`          | Quit the program                     |

Open works with known sites (youtube, google, github, gmail, whatsapp, ...),
installed apps (notepad, kalkulator, chrome, spotify, pengaturan, ...), and any
domain you say (for example "buka github.com").

**Point and speak.** To open a specific link, video, or button, hover the mouse
over it and say `klik` (or "buka ini", "buka yang ditunjuk kursor"). The click
lands wherever the pointer is, so anything on screen can be opened by voice.
This takes priority over site names, so "buka youtube yang ditunjuk kursor"
clicks that video instead of opening the YouTube home page.

**Phrasing is forgiving.** Speech recognition often mangles the verb but gets
the target right, so if a known name appears anywhere in what you said, it
opens. "Halo jalan kan youtube dong" still opens YouTube. An explicit search
verb ("cari ...") always wins, so "cari video youtube" searches instead.

## Requirements

- **Windows, macOS, or Linux.** Fully tested on Windows; macOS and Linux use
  standard tools (`open`/`xdg-open`, `osascript`/`pactl`, `say`/`espeak`) and
  degrade gracefully when one is missing.
- **Python 3.10 or newer** (tested on 3.14).
- A microphone.
- Internet on the first run only, to download the Whisper model once.

## Setup

```sh
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Run

Double click `run.bat`, or from the terminal:

```sh
.venv\Scripts\python -m voice_control
```

The first run downloads the Whisper model (a few minutes). After that it prints
`Siap.` and starts listening. Speak a command, and it acts and replies. Press
`Ctrl+C` or say `berhenti` to stop.

## Configuration

Set environment variables before running to tune behavior:

| Variable          | Default | Meaning                                             |
| :---------------- | :------ | :-------------------------------------------------- |
| `VOICE_MODEL`     | `base`  | Whisper size: `tiny`, `base`, `small`, `medium`     |
| `VOICE_LANG`      | (auto)  | Force a language, for example `id`; empty auto-detects |
| `VOICE_THRESHOLD` | `0.012` | Microphone sensitivity; raise it in a noisy room    |
| `VOICE_SPEAK`     | `1`     | Set to `0` to disable the spoken reply              |

Bigger models understand more languages more accurately but run slower. If
recognition feels weak, try `VOICE_MODEL=small`.

## Project structure

```
voice_control/
  __main__.py     entry point: the listen -> understand -> act loop
  config.py       settings (model, thresholds, language)
  listener.py     microphone capture + voice activity detection
  transcriber.py  Whisper speech to text (auto language)
  intents.py      transcript -> command
  actions.py      map a command to an action (platform neutral)
  system_ops.py   all OS-specific behavior (Windows / macOS / Linux)
  speech.py       spoken reply
requirements.txt
run.bat           convenience launcher
```

## Adding a command

Two small edits: add keywords in `voice_control/intents.py` and handle the new
action in `voice_control/actions.py`.

## Notes and limits

- Speech recognition runs locally after the one-time model download. No audio
  leaves the machine.
- All OS-specific behavior is isolated in `voice_control/system_ops.py`. Windows
  is fully tested; macOS and Linux are best-effort through standard tools.
- App names in `APPS` are tuned for Windows. On macOS and Linux an unknown app
  name simply falls back to a web search, so nothing breaks.
- Recognition quality depends on the model size and your microphone.
- **Media playing through your speakers is heard by the microphone.** The noise
  floor adapts automatically, audio captured while the system is speaking is
  discarded, and the phrases Whisper tends to invent from music are filtered
  out. Even so, speak a little louder than the music, or use headphones.
- Reading the screen means reading window titles, not the pixels. It needs no
  extra permissions and no screenshots are taken.

## Security

- Voice input is never passed to a shell. Every subprocess call uses argument
  lists (never `shell=True`), URLs are percent-encoded or drawn from a fixed
  allow-list, and app targets come only from the fixed `APPS` table.
- The system performs no destructive actions (no delete, format, or shutdown).
- Each command runs inside a guard, so a single failure can never crash the loop.

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Author

**Damta Noviyan Muhamad Faiz**
GitHub: [@damta8827773](https://github.com/damta8827773)
