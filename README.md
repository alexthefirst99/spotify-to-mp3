# Spotify → iPod

Download Spotify playlists and tracks as MP3 files. Built for transferring music to an iPod nano (or any device that takes MP3s).

## Requirements

- Python 3.8+
- macOS (uses Chrome cookies for age-restricted videos)

## Usage

```bash
./run.sh
```

On first run this will install all dependencies and open the app at `http://127.0.0.1:5001` automatically.

## How it works

1. Paste a Spotify playlist or track URL into the app
2. Choose where to save the files (default: `~/Downloads/Spotify_MP3`)
3. Click **Download Songs**

Songs are found on YouTube Music (matched by ISRC code), with YouTube and SoundCloud as fallbacks. Already-downloaded songs are skipped automatically on re-runs.

## Features

- Playlist and single track support
- Skip songs already in the output folder
- Live per-song progress in the browser
- Multiple audio source fallbacks (YouTube Music → YouTube → SoundCloud)
- Age-restricted video support via Chrome cookies
- Open output folder directly from the app

## Known limitations

- **Liked Songs** playlist is private and cannot be accessed — copy songs into a regular playlist first
- Some songs may fail if geo-blocked in your region or unavailable on all providers
- Songs with non-Latin titles (e.g. Chinese characters) may occasionally not match
- Downloads take roughly 30–45 seconds per song

## Files

```
run.sh          — start the app (handles all setup)
app.py          — Flask backend
templates/
  index.html    — web UI
```

## Transferring to iPod

1. Open **Finder** → connect your iPod via USB
2. Click the iPod in the sidebar → **Music**
3. Drag MP3 files from `~/Downloads/Spotify_MP3` into the music list
