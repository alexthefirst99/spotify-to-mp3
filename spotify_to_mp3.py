#!/usr/bin/env python3
"""
spotify_to_mp3.py
Download every song in a Spotify playlist as MP3 using yt-dlp.

Usage:
    python spotify_to_mp3.py <spotify_playlist_url> [--output ./downloads]
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except ImportError:
    print("Missing dependency. Run:  pip install -r requirements.txt")
    sys.exit(1)

load_dotenv()


def get_playlist_tracks(playlist_url: str) -> list[dict]:
    """Return list of {title, artist, album} dicts from a Spotify playlist."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        print(
            "\nSpotify credentials not found.\n"
            "1. Copy .env.example to .env\n"
            "2. Fill in your credentials from https://developer.spotify.com/dashboard\n"
        )
        sys.exit(1)

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )

    # Extract playlist ID from URL (handles /playlist/ID and /playlist/ID?si=...)
    match = re.search(r"playlist/([A-Za-z0-9]+)", playlist_url)
    if not match:
        print(f"Could not parse playlist ID from URL: {playlist_url}")
        sys.exit(1)

    playlist_id = match.group(1)
    tracks = []
    offset = 0

    print(f"Fetching playlist tracks from Spotify...")
    while True:
        results = sp.playlist_tracks(
            playlist_id,
            offset=offset,
            fields="items(track(name,artists,album(name))),next",
        )
        items = results.get("items", [])
        if not items:
            break

        for item in items:
            track = item.get("track")
            if not track:
                continue
            title = track["name"]
            artist = ", ".join(a["name"] for a in track["artists"])
            album = track["album"]["name"]
            tracks.append({"title": title, "artist": artist, "album": album})

        if not results.get("next"):
            break
        offset += len(items)

    return tracks


def sanitize_filename(name: str) -> str:
    """Remove characters that are invalid in file names."""
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def download_track(track: dict, output_dir: Path, index: int, total: int) -> bool:
    """Search YouTube and download a single track as MP3. Returns True on success."""
    title = track["title"]
    artist = track["artist"]
    search_query = f"{artist} - {title} audio"
    safe_name = sanitize_filename(f"{artist} - {title}")

    print(f"\n[{index}/{total}] {artist} - {title}")

    cmd = [
        "yt-dlp",
        f"ytsearch1:{search_query}",   # take the top YouTube search result
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",         # best quality VBR
        "--output", str(output_dir / f"{safe_name}.%(ext)s"),
        "--no-playlist",
        "--quiet",
        "--no-warnings",
        "--progress",
    ]

    try:
        result = subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"  ! Failed to download: {artist} - {title}")
        return False
    except FileNotFoundError:
        print(
            "\nyt-dlp not found. Install it with:\n"
            "  pip install yt-dlp\n"
            "  or\n"
            "  brew install yt-dlp\n"
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Download a Spotify playlist as MP3 files via YouTube."
    )
    parser.add_argument("playlist_url", help="Spotify playlist URL")
    parser.add_argument(
        "--output",
        "-o",
        default="./downloads",
        help="Output folder (default: ./downloads)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    tracks = get_playlist_tracks(args.playlist_url)
    total = len(tracks)
    print(f"Found {total} tracks. Saving MP3s to: {output_dir}\n")

    succeeded, failed = 0, []
    for i, track in enumerate(tracks, start=1):
        ok = download_track(track, output_dir, i, total)
        if ok:
            succeeded += 1
        else:
            failed.append(f"{track['artist']} - {track['title']}")

    print(f"\n{'='*50}")
    print(f"Done! {succeeded}/{total} tracks downloaded.")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
    print(f"\nFiles saved to: {output_dir}")


if __name__ == "__main__":
    main()
