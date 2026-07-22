"""Cross-platform system operations.

All OS-specific behavior is isolated here so the rest of the program stays
platform-neutral. Fully tested on Windows; macOS and Linux use standard tools
(open / xdg-open, osascript / pactl, say / espeak) and degrade gracefully when
a tool is missing. No function here ever raises: each returns a boolean (or
None) so a failed action can never crash the listen loop.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import webbrowser

_SYSTEM = platform.system()
IS_WINDOWS = _SYSTEM == "Windows"
IS_MAC = _SYSTEM == "Darwin"
IS_LINUX = not IS_WINDOWS and not IS_MAC

OS_NAME = _SYSTEM or "Unknown"


def _run(args: list[str]) -> bool:
    """Launch a detached process without raising. True if it started."""
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


# --- Browser ------------------------------------------------------------------
def _find_chrome() -> str | None:
    if IS_WINDOWS:
        for path in (
            os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"),
                         "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                         "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""),
                         "Google", "Chrome", "Application", "chrome.exe"),
        ):
            if path and os.path.isfile(path):
                return path
    elif IS_MAC:
        path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.isfile(path):
            return path
    else:
        for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
            found = shutil.which(name)
            if found:
                return found
    return shutil.which("chrome")


_CHROME = _find_chrome()


def open_url(url: str) -> bool:
    """Open a URL, preferring Chrome, falling back to the default browser."""
    if _CHROME and _run([_CHROME, url]):
        return True
    try:
        return bool(webbrowser.open(url))
    except Exception:
        return False


# --- Apps / protocols ---------------------------------------------------------
def open_target(target: str) -> bool:
    """Open an app name, protocol, or path through the OS launcher."""
    if IS_WINDOWS:
        return _run(["cmd", "/c", "start", "", target])
    if IS_MAC:
        return _run(["open", target])
    return _run(["xdg-open", target])


# --- Volume -------------------------------------------------------------------
def _win_volume(vk: int, times: int) -> bool:
    try:
        import ctypes

        for _ in range(times):
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)  # key down
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)  # key up
        return True
    except Exception:
        return False


def volume_up() -> bool:
    if IS_WINDOWS:
        return _win_volume(0xAF, 5)
    if IS_MAC:
        return _run(["osascript", "-e",
                     "set volume output volume (output volume of (get volume settings) + 12)"])
    return _run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"])


def volume_down() -> bool:
    if IS_WINDOWS:
        return _win_volume(0xAE, 5)
    if IS_MAC:
        return _run(["osascript", "-e",
                     "set volume output volume (output volume of (get volume settings) - 12)"])
    return _run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"])


def mute() -> bool:
    if IS_WINDOWS:
        return _win_volume(0xAD, 1)
    if IS_MAC:
        return _run(["osascript", "-e", "set volume with output muted"])
    return _run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])


# --- Lock screen --------------------------------------------------------------
def lock_screen() -> bool:
    if IS_WINDOWS:
        try:
            import ctypes

            ctypes.windll.user32.LockWorkStation()
            return True
        except Exception:
            return False
    if IS_MAC:
        return _run(["pmset", "displaysleepnow"])
    if shutil.which("loginctl") and _run(["loginctl", "lock-session"]):
        return True
    return _run(["xdg-screensaver", "lock"])


# --- Text to speech -----------------------------------------------------------
def speak(text: str) -> None:
    if not text:
        return
    try:
        if IS_WINDOWS:
            safe = text.replace("'", "''")
            script = (
                "Add-Type -AssemblyName System.Speech;"
                "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
                f"$s.Speak('{safe}')"
            )
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", script],
                timeout=15, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        elif IS_MAC:
            subprocess.run(["say", text], timeout=15,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            tool = shutil.which("spd-say") or shutil.which("espeak")
            if tool:
                subprocess.run([tool, text], timeout=15,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Speaking is best effort; never let it crash the loop.
        pass
