# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

spotdl_datas, spotdl_binaries, spotdl_hidden = collect_all('spotdl')
ytdlp_hidden = collect_submodules('yt_dlp')

a = Analysis(
    ['app.py'],
    binaries=spotdl_binaries,
    datas=[
        ('templates', 'templates'),
        *spotdl_datas,
    ],
    hiddenimports=[
        *spotdl_hidden,
        *ytdlp_hidden,
        'flask',
        'spotipy',
        'mutagen',
        'mutagen.mp3',
        'mutagen.id3',
        'mutagen.mp4',
        'mutagen.flac',
        'mutagen.oggvorbis',
        'requests',
        'certifi',
        'charset_normalizer',
        'idna',
        'urllib3',
        'syncedlyrics',
        'Crypto',
        'Crypto.Cipher',
        'Crypto.Cipher.AES',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'unittest'],
    noarchive=False,
)

pyz = PYZ(a.pure)

EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Spotify to MP3',
    debug=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)
