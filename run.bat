@echo off
REM Launch Sistem Otomasi Suara using the project virtual environment.
cd /d "%~dp0"
".venv\Scripts\python.exe" -m voice_control %*
