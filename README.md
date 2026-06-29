# Spotify to MP3

Download Spotify playlists and tracks as MP3 files. Works with any MP3 player.

## Download (Windows, no install needed)

Go to [Releases](../../releases/latest) and download **Spotify to MP3.exe**. Double-click to launch — no Python, no setup.

## Mac / Windows with Python

**Mac** — double-click `run.command`

**Windows** — double-click `run.bat`

The app opens in your browser at `http://127.0.0.1:5001`. Python must be installed — the script handles everything else automatically on first run.

## Spotify API setup

Spotify playlist metadata requires a free Spotify Developer app:

1. Go to https://developer.spotify.com/dashboard and create an app
2. Add this redirect URI in the app settings:

```
http://127.0.0.1:9900/
```

3. Copy `.env.example` to `.env`
4. Paste your app credentials into `.env`:

```
SPOTIPY_CLIENT_ID=...
SPOTIPY_CLIENT_SECRET=...
```

This avoids spotDL's public bundled credentials, which can get rate-limited and cause errors like `Could not get general hashes`.
The first download may open a Spotify authorization page. Log in and approve it once; the token is cached for future runs.

## How to use

1. Copy a Spotify playlist or track URL
2. Paste it into the app and click **Download Songs**

Songs are saved as MP3 files in your Downloads folder. Songs already downloaded are skipped automatically.

### Wrong version downloaded?

Use the **Download from YouTube URL** card at the bottom:

1. Copy the Spotify track URL for correct metadata
2. Find the right version on YouTube, copy that URL
3. Paste both — the app downloads the YouTube audio with the Spotify album art and tags

## Known limitations

- **Liked Songs** cannot be downloaded — it's a private playlist. Move songs into a regular playlist first
- Songs may fail if geo-blocked or unavailable on all providers
- Each song takes roughly 30–45 seconds to download

## Files

```
run.command           launch on Mac (requires Python)
run.bat               launch on Windows (requires Python)
build.bat             build the .exe (requires Python, for developers only)
app.py                backend
templates/index.html  web UI
spotify_to_mp3.spec   PyInstaller config
```
