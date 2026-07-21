"""Execute an Intent on the laptop. Every action here touches the real system:
opening apps and sites, controlling volume, locking the screen."""

from __future__ import annotations

import ctypes
import re
import subprocess
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote

from .intents import Intent


@dataclass
class ActionResult:
    ok: bool
    message: str


# Spoken name -> website.
SITES: dict[str, str] = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://instagram.com",
    "tiktok": "https://tiktok.com",
    "maps": "https://maps.google.com",
    "chatgpt": "https://chat.openai.com",
}

# Spoken name -> launch target understood by the Windows shell `start`.
APPS: dict[str, str] = {
    "notepad": "notepad",
    "kalkulator": "calc",
    "calculator": "calc",
    "paint": "mspaint",
    "explorer": "explorer",
    "file": "explorer",
    "folder": "explorer",
    "cmd": "cmd",
    "chrome": "chrome",
    "edge": "msedge",
    "spotify": "spotify:",
    "kamera": "microsoft.windows.camera:",
    "camera": "microsoft.windows.camera:",
    "pengaturan": "ms-settings:",
    "settings": "ms-settings:",
}

# Virtual key codes for media volume keys.
_VK_VOLUME_MUTE = 0xAD
_VK_VOLUME_DOWN = 0xAE
_VK_VOLUME_UP = 0xAF


def _start(target: str) -> None:
    # `start` resolves app names on PATH, protocols (ms-settings:) and URLs.
    subprocess.Popen(["cmd", "/c", "start", "", target])


def _tap_key(vk: int, times: int = 1) -> None:
    for _ in range(times):
        ctypes.windll.user32.keybd_event(vk, 0, 0, 0)  # key down
        ctypes.windll.user32.keybd_event(vk, 0, 2, 0)  # key up


def execute(intent: Intent, lang: str | None) -> ActionResult:
    is_id = (lang or "id").startswith("id")

    def msg(indonesian: str, english: str) -> str:
        return indonesian if is_id else english

    action = intent.action
    arg = intent.arg.strip()

    if action == "open_site":
        if not arg:
            return ActionResult(False, msg("Mau buka apa?", "Open what?"))
        # Scan the words for a known app, site, or domain so filler words like
        # "coba dong" or "tolong" do not break the match.
        for word in re.findall(r"[a-z0-9.]+", arg.lower()):
            if word in APPS:
                _start(APPS[word])
                return ActionResult(True, msg(f"Membuka {word}", f"Opening {word}"))
            if word in SITES:
                webbrowser.open(SITES[word])
                return ActionResult(True, msg(f"Membuka {word}", f"Opening {word}"))
            if "." in word and len(word) > 3:
                webbrowser.open("https://" + word)
                return ActionResult(True, msg(f"Membuka {word}", f"Opening {word}"))
        # Nothing recognized: search for it instead of failing with a shell error.
        webbrowser.open("https://www.google.com/search?q=" + quote(arg))
        return ActionResult(
            True, msg(f"Tidak ketemu aplikasinya, mencari {arg}", f"Not found, searching {arg}")
        )

    if action == "search":
        if not arg:
            return ActionResult(False, msg("Mau cari apa?", "Search for what?"))
        webbrowser.open("https://www.google.com/search?q=" + quote(arg))
        return ActionResult(True, msg(f"Mencari {arg}", f"Searching {arg}"))

    if action == "time":
        now = datetime.now().strftime("%H:%M")
        return ActionResult(True, msg(f"Sekarang pukul {now}", f"It is {now}"))

    if action == "date":
        today = datetime.now().strftime("%A, %d %B %Y")
        return ActionResult(True, msg(f"Hari ini {today}", f"Today is {today}"))

    if action == "volume_up":
        _tap_key(_VK_VOLUME_UP, 5)
        return ActionResult(True, msg("Volume dinaikkan", "Volume up"))

    if action == "volume_down":
        _tap_key(_VK_VOLUME_DOWN, 5)
        return ActionResult(True, msg("Volume diturunkan", "Volume down"))

    if action == "mute":
        _tap_key(_VK_VOLUME_MUTE)
        return ActionResult(True, msg("Suara dibisukan", "Muted"))

    if action == "lock":
        ctypes.windll.user32.LockWorkStation()
        return ActionResult(True, msg("Mengunci layar", "Locking the screen"))

    if action == "help":
        return ActionResult(
            True,
            msg(
                "Coba: buka youtube, cari resep nasi goreng, jam berapa, volume naik, kunci layar, berhenti.",
                "Try: open youtube, search fried rice, what time, volume up, lock screen, stop.",
            ),
        )

    if action == "quit":
        return ActionResult(True, msg("Menghentikan sistem", "Stopping"))

    return ActionResult(
        False, msg(f"Perintah tidak dikenali: {intent.raw}", f"Command not recognized: {intent.raw}")
    )
