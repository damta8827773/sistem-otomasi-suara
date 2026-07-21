<div align="center">

# Sistem Otomasi Suara

A terminal voice controller for your laptop. Run it, speak, and your computer
acts. Say "buka youtube" and YouTube opens. Say "kunci layar" and the screen
locks. It understands any language, because it transcribes with Whisper.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Whisper](https://img.shields.io/badge/STT-faster--whisper-5A45FF)](https://github.com/SYSTRAN/faster-whisper)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)](#)
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
| `volume naik` / `volume down`| Change the system volume             |
| `bisukan` / `mute`           | Mute the sound                       |
| `kunci layar` / `lock screen`| Lock the workstation                 |
| `bantuan` / `help`           | List commands out loud               |
| `berhenti` / `stop`          | Quit the program                     |

Open works with known sites (youtube, google, github, gmail, whatsapp, ...),
installed apps (notepad, kalkulator, chrome, spotify, pengaturan, ...), and any
domain you say (for example "buka github.com").

## Requirements

- **Windows** (uses Windows shell, volume keys, screen lock, and the SAPI voice).
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
  actions.py      run the command on the laptop
  speech.py       spoken reply (Windows SAPI)
requirements.txt
run.bat           convenience launcher
```

## Adding a command

Two small edits: add keywords in `voice_control/intents.py` and handle the new
action in `voice_control/actions.py`.

## Notes and limits

- Speech recognition runs locally after the one-time model download. No audio
  leaves the machine.
- Actions are Windows specific. Porting to macOS or Linux means changing
  `actions.py` (volume keys, screen lock) and `speech.py`.
- Recognition quality depends on the model size and your microphone.

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Author

**Damta Noviyan Muhamad Faiz**
GitHub: [@damta8827773](https://github.com/damta8827773)
