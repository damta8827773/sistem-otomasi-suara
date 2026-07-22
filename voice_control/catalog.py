"""Known open targets: spoken names mapped to sites and apps. Shared by the
intent parser (to detect a target anywhere in a phrase) and the action layer
(to actually open it)."""

from __future__ import annotations

# Spoken name -> website.
SITES: dict[str, str] = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "tiktok": "https://tiktok.com",
    "twitter": "https://twitter.com",
    "maps": "https://maps.google.com",
    "chatgpt": "https://chat.openai.com",
}

# Spoken name -> app launch target. Values are tuned for Windows; on macOS and
# Linux the OS launcher resolves what it can and unknown names fall back to a
# web search.
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

# Every spoken name we recognize as an "open this" target.
KNOWN_TARGETS: frozenset[str] = frozenset(SITES) | frozenset(APPS)
