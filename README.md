# Spotify to MP3

Download Spotify playlists and tracks as MP3 files.

## Quick start

**Mac** — double-click `run.command`

**Windows** — double-click `run.bat`

The app opens in your browser at `http://127.0.0.1:5001`. Python must be installed — the script handles everything else automatically on first run.

> Don't have Python? Use the standalone app below — no installs needed.

## How to use

1. Copy a Spotify playlist or track URL
2. Paste it into the app
3. Click **Download Songs**

Songs are matched by ISRC code on YouTube Music, with YouTube and SoundCloud as fallbacks. Songs already in the output folder are skipped automatically.

## Standalone app for Windows (no Python required)

Double-click `build.bat` to build. Output: `dist\Spotify to MP3.exe`

The `.exe` is ~150–200 MB and includes everything bundled inside. Right-click → **Send to → Desktop (create shortcut)** for easy access.

## Known limitations

- **Liked Songs** is a private playlist and cannot be downloaded — move songs into a regular playlist first
- Songs may fail if geo-blocked in your region or unavailable on all providers
- Songs with non-Latin titles may occasionally fail to match
- Each song takes roughly 30–45 seconds to download

## Files

```
run.command           double-click to launch on Mac (requires Python)
run.bat               double-click to launch on Windows (requires Python)
build.bat             build standalone .exe for Windows (no Python needed)
app.py                backend
templates/index.html  web UI
spotify_to_mp3.spec   PyInstaller config (for building)
```
