@echo off
title Spotify to MP3
cd /d "%~dp0"

echo.
echo Spotify to MP3
echo ==========================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 not found.
    echo         Install from: https://python.org/downloads
    echo         Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo [OK] Python %%v

:: Install packages if missing
python -c "import spotdl, flask" >nul 2>&1
if errorlevel 1 (
    echo Installing packages (first run only)...
    pip install spotdl flask yt-dlp -q --disable-pip-version-check
    if errorlevel 1 (
        echo [ERROR] Package install failed. Try running as Administrator.
        pause
        exit /b 1
    )
)
echo Updating download tools...
pip install -U spotdl yt-dlp -q --disable-pip-version-check
echo [OK] Packages ready

:: Install Deno for YouTube Music support
python -m spotdl --download-deno >nul 2>&1
echo [OK] YouTube Music support ready

echo.
echo Opening at http://127.0.0.1:5001
echo.
python app.py
pause
