from __future__ import annotations
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def wait_for_track_start(sp: spotipy.Spotify, track_id: str) -> float:
    while True:
        p = sp.currently_playing()
        if p and p.get("is_playing") and p.get("item") and p["item"]["id"] == track_id and p.get("progress_ms", 9999) < 500:
            return time.perf_counter()
        time.sleep(0.5)