"""Turn a transcript into an Intent by keyword matching. Keywords cover several
languages (Indonesian and English by default); add more freely."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Intent:
    action: str
    arg: str = ""
    raw: str = ""


# Commands that capture the words after the keyword as an argument.
CAPTURE_COMMANDS: dict[str, list[str]] = {
    "open_site": ["buka", "bukakan", "open", "launch"],
    "search": ["cari", "carikan", "search", "find", "googling"],
}

# Commands triggered by a phrase, no argument. Multi word phrases first.
SIMPLE_COMMANDS: dict[str, list[str]] = {
    "time": ["jam berapa", "what time", "waktu sekarang"],
    "date": ["tanggal berapa", "hari apa", "what date", "what day"],
    "volume_up": ["volume naik", "perbesar suara", "volume up", "louder"],
    "volume_down": ["volume turun", "perkecil suara", "volume down", "quieter"],
    "mute": ["bisukan", "senyapkan", "mute"],
    "lock": ["kunci layar", "kunci laptop", "lock screen", "lock"],
    "help": ["bantuan", "perintah apa saja", "help", "what can you do"],
    "quit": ["berhenti", "keluar program", "stop listening", "exit", "quit"],
}

_STRIP = " .,!?;:"


def parse_intent(text: str) -> Intent:
    raw = text.strip()
    low = raw.lower().strip(_STRIP)

    for action, keywords in CAPTURE_COMMANDS.items():
        for keyword in keywords:
            if low.startswith(keyword + " "):
                arg = raw[len(keyword):].strip(_STRIP).strip()
                return Intent(action, arg, raw)

    for action, keywords in SIMPLE_COMMANDS.items():
        for keyword in keywords:
            if low == keyword or keyword in low:
                return Intent(action, "", raw)

    return Intent("unknown", "", raw)
