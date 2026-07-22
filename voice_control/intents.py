"""Turn a transcript into an Intent.

Speech recognition often mangles the command verb (for example "buka" becomes
"jalan kan" or "mana"), but the target word ("youtube") is usually correct. So
the parser is forgiving: if a known site or app name appears anywhere in the
phrase, it opens it, even when the verb was misheard.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .catalog import KNOWN_TARGETS

# Verbs that mean "open / launch / play this".
OPEN_VERBS = (
    "buka", "bukain", "bukakan", "jalankan", "mainkan", "putar", "play",
    "open", "launch", "jalan",
)

# Verbs that mean "search the web for this". Note: "google" is intentionally
# NOT here, since "buka google" should open the site, not search.
SEARCH_VERBS = ("cari", "carikan", "search", "find", "googling", "telusuri")

# Phrase commands with no argument. Multi-word entries are matched as a phrase;
# single words are matched on a word boundary to avoid false substrings.
SIMPLE_COMMANDS: dict[str, list[str]] = {
    "time": ["jam berapa", "what time", "waktu sekarang"],
    "date": ["tanggal berapa", "hari apa", "what date", "what day"],
    "volume_up": ["volume naik", "perbesar suara", "volume up", "louder"],
    "volume_down": ["volume turun", "perkecil suara", "volume down", "quieter"],
    "mute": ["bisukan", "senyapkan", "mute"],
    "lock": ["kunci layar", "kunci laptop", "lock screen", "lock"],
    "windows_list": ["daftar jendela", "apa saja yang terbuka", "semua jendela",
                     "list windows", "open windows"],
    "screen": ["layar apa", "sedang buka apa", "lagi buka apa", "jendela apa",
               "baca layar", "what is on screen", "active window"],
    "help": ["bantuan", "perintah apa saja", "help", "what can you do"],
    "quit": ["berhenti", "keluar program", "stop listening", "exit", "quit"],
}

# Phrases Whisper commonly invents from music or background noise. They are
# never real commands, so they are dropped before parsing.
NOISE_PHRASES = frozenset({
    "terima kasih", "terima kasih banyak", "terimakasih",
    "thank you", "thanks for watching", "thank you for watching",
    "silakan berlangganan", "jangan lupa subscribe", "subscribe",
    "sampai jumpa", "bye", "you", "hmm", "oke", "ok", "ya", "iya",
})


def is_probably_noise(text: str) -> bool:
    """True when the transcript is almost certainly background noise."""
    low = _normalize(text)
    return not low or low in NOISE_PHRASES or len(low) <= 2


@dataclass
class Intent:
    action: str
    arg: str = ""
    raw: str = ""


def _normalize(text: str) -> str:
    # Lower case, keep dots (for domains), turn other punctuation into spaces.
    low = re.sub(r"[^\w\s.]", " ", text.lower())
    return re.sub(r"\s+", " ", low).strip()


def _after(words: list[str], verb: str) -> str:
    try:
        index = words.index(verb)
    except ValueError:
        return ""
    return " ".join(words[index + 1:]).strip()


def parse_intent(text: str) -> Intent:
    raw = text.strip()
    low = _normalize(raw)
    words = low.split()

    # 1. Explicit search verb wins first, so "cari video youtube" searches
    #    rather than opening YouTube.
    for verb in SEARCH_VERBS:
        if verb in words:
            arg = _after(words, verb)
            if arg:
                return Intent("search", arg, raw)

    # 2. Phrase commands (time, date, volume, lock, help, quit).
    for action, phrases in SIMPLE_COMMANDS.items():
        for phrase in phrases:
            hit = phrase in low if " " in phrase else phrase in words
            if hit:
                return Intent(action, "", raw)

    # 3. A known site or app named anywhere -> open it, even if the verb was
    #    misheard. This is what makes "buka youtube" robust.
    for word in words:
        name = word.strip(".")
        if name in KNOWN_TARGETS:
            return Intent("open_site", name, raw)

    # 4. An open verb followed by something (a domain, or an unknown name that
    #    will fall back to a web search in the action layer).
    for verb in OPEN_VERBS:
        if verb in words:
            arg = _after(words, verb)
            if arg:
                return Intent("open_site", arg, raw)

    return Intent("unknown", "", raw)
