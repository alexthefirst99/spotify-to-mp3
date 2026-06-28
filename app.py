#!/usr/bin/env python3
from flask import Flask, render_template, request, Response, jsonify
import threading
import queue
import uuid
import json
import os
import sys
import subprocess
from pathlib import Path

from spotdl import Spotdl
from spotdl.utils.spotify import SpotifyClient
from spotdl.utils.config import DEFAULT_CONFIG
from spotdl.utils.formatter import create_file_name
from spotdl.types.playlist import Playlist
from spotdl.types.song import Song

# Resolve base directory — handles source, onefile bundle, and onedir .app bundle
if getattr(sys, "frozen", False):
    _BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
else:
    _BASE_DIR = Path(__file__).parent

app = Flask(__name__, template_folder=str(_BASE_DIR / "templates"))
_jobs = {}
_spotdl_lock = threading.Lock()  # one download at a time (spotdl has a global spotify singleton)

# Use spotdl's own bundled credentials — no user setup required
_CLIENT_ID = DEFAULT_CONFIG["client_id"]
_CLIENT_SECRET = DEFAULT_CONFIG["client_secret"]


_OUTPUT_TEMPLATE = "{artists} - {title}.{output-ext}"


def _make_spotdl(out_dir: str) -> Spotdl:
    SpotifyClient._instance = None  # reset singleton so we can reinit with fresh settings
    return Spotdl(
        client_id=_CLIENT_ID,
        client_secret=_CLIENT_SECRET,
        headless=True,
        no_cache=True,
        downloader_settings={
            "output": str(Path(out_dir) / _OUTPUT_TEMPLATE),
            "format": "mp3",
            "bitrate": "auto",
            "overwrite": "skip",
            "threads": 1,
            "audio_providers": ["youtube-music", "youtube", "soundcloud"],
            "cookie_file": None,
            "yt_dlp_args": "--cookies-from-browser chrome",
            "simple_tui": True,
        },
    )


def _already_downloaded(out_dir: str, song) -> bool:
    """Return True if the song's MP3 already exists in the output folder."""
    try:
        template = str(Path(out_dir) / _OUTPUT_TEMPLATE)
        path = create_file_name(song, template, "mp3")
        return path.exists()
    except Exception:
        return False


def _worker(job_id: str, url: str, out_dir: str):
    q = _jobs[job_id]

    def emit(d):
        q.put(json.dumps(d))

    with _spotdl_lock:
        try:
            client = _make_spotdl(out_dir)

            if "/track/" in url:
                emit({"type": "status", "msg": "Fetching song from Spotify…"})
                track_urls = [url]
            else:
                emit({"type": "status", "msg": "Fetching playlist from Spotify…"})
                playlist = Playlist.from_url(url, fetch_songs=False)
                track_urls = playlist.urls

            if not track_urls:
                raise ValueError("No songs found. Double-check the URL.")

            total = len(track_urls)
            emit({"type": "start", "total": total})
            Path(out_dir).mkdir(parents=True, exist_ok=True)

            ok_count = 0
            skipped_count = 0
            failed = []

            for i, track_url in enumerate(track_urls, 1):
                # Fetch metadata for this one song, then download immediately
                try:
                    song = Song.from_url(track_url)
                except Exception:
                    emit({"type": "track_start", "i": i, "total": total,
                          "title": "Unknown track", "artist": ""})
                    emit({"type": "track_done", "i": i, "ok": False})
                    failed.append(f"Track {i}")
                    continue

                emit({"type": "track_start", "i": i, "total": total,
                      "title": song.name, "artist": song.artist})

                if _already_downloaded(out_dir, song):
                    skipped_count += 1
                    emit({"type": "track_done", "i": i, "ok": True, "skipped": True})
                    continue

                try:
                    _, path = client.download(song)
                    if path:
                        ok_count += 1
                        emit({"type": "track_done", "i": i, "ok": True, "skipped": False})
                    else:
                        failed.append(f"{song.artist} – {song.name}")
                        emit({"type": "track_done", "i": i, "ok": False})
                except Exception:
                    failed.append(f"{song.artist} – {song.name}")
                    emit({"type": "track_done", "i": i, "ok": False})

            emit({"type": "complete", "ok": ok_count, "skipped": skipped_count,
                  "total": total, "failed": failed, "out": out_dir})

        except Exception as e:
            emit({"type": "error", "msg": str(e)})
        finally:
            q.put(None)


@app.route("/")
def index():
    default_out = str(Path.home() / "Downloads" / "Spotify_MP3")
    return render_template("index.html", default_out=default_out)


@app.route("/start", methods=["POST"])
def start():
    d = request.get_json(force=True) or {}
    url = (d.get("url") or "").strip()
    out = (d.get("out") or "").strip() or str(Path.home() / "Downloads" / "Spotify_MP3")
    if not url:
        return jsonify(error="Paste a Spotify playlist URL first."), 400
    jid = str(uuid.uuid4())
    _jobs[jid] = queue.Queue()
    threading.Thread(target=_worker, args=(jid, url, out), daemon=True).start()
    return jsonify(job_id=jid)


@app.route("/progress/<jid>")
def progress(jid):
    if jid not in _jobs:
        return "Not found", 404

    def gen():
        q = _jobs[jid]
        while True:
            item = q.get()
            if item is None:
                yield "data: [DONE]\n\n"
                break
            yield f"data: {item}\n\n"
        _jobs.pop(jid, None)

    return Response(
        gen(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/open", methods=["POST"])
def open_folder():
    d = request.get_json(force=True) or {}
    path = d.get("path", "")
    if path and os.path.isdir(path):
        if sys.platform == "win32":
            subprocess.Popen(["explorer", path])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    return "", 204


if __name__ == "__main__":
    import webbrowser

    # Download Deno for YouTube Music support (skips if already installed)
    try:
        from spotdl.utils.deno import download_deno, is_deno_installed
        if not is_deno_installed():
            print("Downloading Deno for YouTube Music support (one-time setup)...")
            download_deno()
    except Exception:
        pass

    threading.Timer(0.8, lambda: webbrowser.open("http://127.0.0.1:5001")).start()
    print("Starting Spotify to MP3 at http://127.0.0.1:5001")
    app.run(port=5001, threaded=True)
