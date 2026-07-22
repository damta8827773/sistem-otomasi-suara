"""Execute an Intent on the laptop. Every action here touches the real system:
opening apps and sites, controlling volume, locking the screen.

All OS-specific work is delegated to system_ops, so this module is platform
neutral and every branch fails safely (a failed action returns a message rather
than raising)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote

from . import system_ops
from .catalog import APPS, SITES
from .intents import Intent


@dataclass
class ActionResult:
    ok: bool
    message: str


def _search_url(query: str) -> str:
    return "https://www.google.com/search?q=" + quote(query)


def execute(intent: Intent, lang: str | None) -> ActionResult:
    is_id = (lang or "id").startswith("id")

    def msg(indonesian: str, english: str) -> str:
        return indonesian if is_id else english

    action = intent.action
    arg = intent.arg.strip()

    if action == "open_site":
        if not arg:
            return ActionResult(False, msg("Mau buka apa?", "Open what?"))
        # Scan words for a known app, site, or domain so filler words like
        # "coba dong" or "tolong" do not break the match.
        for word in re.findall(r"[a-z0-9.]+", arg.lower()):
            if word in APPS:
                system_ops.open_target(APPS[word])
                return ActionResult(True, msg(f"Membuka {word}", f"Opening {word}"))
            if word in SITES:
                system_ops.open_url(SITES[word])
                return ActionResult(True, msg(f"Membuka {word}", f"Opening {word}"))
            if "." in word and len(word) > 3:
                system_ops.open_url("https://" + word)
                return ActionResult(True, msg(f"Membuka {word}", f"Opening {word}"))
        # Nothing recognized: search for it instead of failing.
        system_ops.open_url(_search_url(arg))
        return ActionResult(
            True, msg(f"Tidak ketemu aplikasinya, mencari {arg}", f"Not found, searching {arg}")
        )

    if action == "search":
        if not arg:
            return ActionResult(False, msg("Mau cari apa?", "Search for what?"))
        system_ops.open_url(_search_url(arg))
        return ActionResult(True, msg(f"Mencari {arg}", f"Searching {arg}"))

    if action == "time":
        now = datetime.now().strftime("%H:%M")
        return ActionResult(True, msg(f"Sekarang pukul {now}", f"It is {now}"))

    if action == "date":
        today = datetime.now().strftime("%A, %d %B %Y")
        return ActionResult(True, msg(f"Hari ini {today}", f"Today is {today}"))

    if action == "volume_up":
        ok = system_ops.volume_up()
        return ActionResult(ok, msg("Volume dinaikkan", "Volume up") if ok
                            else msg("Gagal mengatur volume", "Could not change volume"))

    if action == "volume_down":
        ok = system_ops.volume_down()
        return ActionResult(ok, msg("Volume diturunkan", "Volume down") if ok
                            else msg("Gagal mengatur volume", "Could not change volume"))

    if action == "mute":
        ok = system_ops.mute()
        return ActionResult(ok, msg("Suara dibisukan", "Muted") if ok
                            else msg("Gagal membisukan", "Could not mute"))

    if action == "lock":
        ok = system_ops.lock_screen()
        return ActionResult(ok, msg("Mengunci layar", "Locking the screen") if ok
                            else msg("Gagal mengunci layar", "Could not lock the screen"))

    if action in ("click", "right_click", "double_click"):
        ok = system_ops.click(
            button="right" if action == "right_click" else "left",
            double=action == "double_click",
        )
        if not ok:
            return ActionResult(False, msg("Gagal mengeklik", "Could not click"))
        label = {
            "click": msg("Diklik", "Clicked"),
            "right_click": msg("Klik kanan", "Right clicked"),
            "double_click": msg("Klik dua kali", "Double clicked"),
        }[action]
        return ActionResult(True, label)

    if action == "screen":
        title = system_ops.active_window_title()
        if not title:
            return ActionResult(False, msg("Tidak bisa membaca layar", "Cannot read the screen"))
        return ActionResult(True, msg(f"Sedang membuka {title}", f"Currently showing {title}"))

    if action == "windows_list":
        titles = system_ops.list_windows(limit=6)
        if not titles:
            return ActionResult(False, msg("Tidak ada jendela terbaca", "No windows detected"))
        listed = ", ".join(titles)
        return ActionResult(True, msg(f"Yang terbuka: {listed}", f"Open windows: {listed}"))

    if action == "help":
        return ActionResult(
            True,
            msg(
                "Coba: buka youtube, klik yang ditunjuk kursor, cari resep nasi goreng, "
                "jam berapa, sedang buka apa, volume naik, kunci layar, berhenti.",
                "Try: open youtube, click what the cursor points at, search fried rice, "
                "what time, what is on screen, volume up, lock screen, stop.",
            ),
        )

    if action == "quit":
        return ActionResult(True, msg("Menghentikan sistem", "Stopping"))

    return ActionResult(
        False, msg(f"Perintah tidak dikenali: {intent.raw}", f"Command not recognized: {intent.raw}")
    )
