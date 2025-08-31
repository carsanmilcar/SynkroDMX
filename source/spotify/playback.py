
from __future__ import annotations

"""Helpers for reading playback information from Spotify."""

import time
from typing import Any, Dict, List, Optional, Tuple
import spotipy

try:
    from spotipy.exceptions import SpotifyException
except Exception:  # pragma: no cover
    SpotifyException = Exception

# Simple cache for genres per artist
_ARTIST_GENRES_CACHE: Dict[str, List[str]] = {}


def get_now_playing(sp: spotipy.Spotify) -> Optional[Dict[str, Any]]:
    """Retrieve playback state.

    1. Attempt ``/me/player`` if the scope permits.
    2. Fallback to ``/me/player/currently-playing`` with a normalized format.
    """
    try:
        pb = sp.current_playback(additional_types="track,episode")
        if pb and pb.get("item"):
            return pb
    except SpotifyException:
        pass
    except Exception:
        pass

    try:
        cp = sp.current_user_playing_track()
        if not cp:
            return None
        return {
            "is_playing": bool(cp.get("is_playing")),
            "progress_ms": cp.get("progress_ms"),
            "timestamp": cp.get("timestamp") or int(time.time() * 1000),
            "item": cp.get("item"),
            "currently_playing_type": cp.get("currently_playing_type") or (cp.get("item") or {}).get("type"),
            "context": None,
        }
    except Exception:
        return None

def get_queue_safe(sp: spotipy.Spotify, max_items: int = 5) -> List[Dict[str, Any]]:
    """Attempt to read ``/me/player/queue``; return ``[]`` on failure or missing scope."""
    try:
        q = sp.queue()
        return (q.get("queue") or [])[:max_items]
    except Exception:
        return []

def _artist_genres(sp: spotipy.Spotify, artist_id: Optional[str]) -> List[str]:
    """Return genres for the main artist with caching."""
    if not artist_id:
        return []
    cached = _ARTIST_GENRES_CACHE.get(artist_id)
    if cached is not None:
        return cached
    try:
        ar = sp.artist(artist_id)
        genres = ar.get("genres") or []
    except Exception:
        genres = []
    _ARTIST_GENRES_CACHE[artist_id] = genres
    return genres


def extract_artist_and_genres(
    sp: spotipy.Spotify,
    item: Dict[str, Any],
    item_type: str,
) -> Tuple[str, Optional[str], List[str]]:
    """Return ``(artist_names_csv, main_artist_id, genres)``.

    For episodes, use the publisher or show name and return empty genres.
    """
    if item_type == "track":
        artists = item.get("artists") or []
        artist_names = ", ".join(a.get("name", "") for a in artists if a.get("name"))
        main_artist_id = artists[0].get("id") if artists else None
        genres = _artist_genres(sp, main_artist_id)
        return artist_names, main_artist_id, genres

    show = item.get("show") or {}
    artist_names = show.get("publisher") or show.get("name") or ""
    return artist_names, None, []
