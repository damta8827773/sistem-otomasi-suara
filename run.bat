@echo off
REM Launch Sistem Otomasi Suara using the project virtual environment.
chcp 65001 >nul
cd /d "%~dp0"
title Sistem Otomasi Suara
".venv\Scripts\python.exe" -u -m voice_control %*
echo.
echo (Sistem berhenti. Tekan tombol apa saja untuk menutup jendela ini.)
pause >nul
