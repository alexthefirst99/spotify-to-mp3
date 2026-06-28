@echo off
title Build Spotify to MP3
cd /d "%~dp0"

echo.
echo Building Spotify to MP3 -- Windows
echo =====================================

echo Installing build tools...
pip install pyinstaller spotdl flask -q --disable-pip-version-check
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
echo Done!
echo App: dist\Spotify to MP3.exe
echo.
echo Double-click the .exe to launch. You can create a desktop shortcut by
echo right-clicking it and selecting "Send to > Desktop (create shortcut)".
pause
