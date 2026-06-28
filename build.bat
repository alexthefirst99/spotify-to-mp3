@echo off
title Build Spotify to MP3
cd /d "%~dp0"

echo.
echo Build Spotify to MP3 -- Windows
echo =====================================
echo This script requires Python. Run it once to produce
echo dist\Spotify to MP3.exe which you can share with anyone.
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo         Install Python from https://python.org/downloads
    echo         and make sure to check "Add Python to PATH" during install.
    echo         Then re-run this script.
    pause & exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo [OK] Python %%v

echo Installing build tools...
pip install pyinstaller spotdl flask yt-dlp -q --disable-pip-version-check
if errorlevel 1 (
    echo [ERROR] Install failed. Try running as Administrator.
    pause & exit /b 1
)

echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo Building .exe (this takes a few minutes)...
pyinstaller spotify_to_mp3.spec --noconfirm
if errorlevel 1 (
    echo [ERROR] Build failed. See output above for details.
    pause & exit /b 1
)

echo.
echo Done! Output: dist\Spotify to MP3.exe
echo.
echo Share that .exe with anyone -- no Python needed to run it.
echo Right-click it and select "Send to > Desktop (create shortcut)" for easy access.
pause
