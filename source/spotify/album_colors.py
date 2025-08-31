from __future__ import annotations

"""Utilities for retrieving album art and extracting color palettes."""

from typing import Dict, List, Optional, Tuple
from io import BytesIO

import requests
import spotipy
from colorthief import ColorThief

from .playback import get_now_playing


RGB = Tuple[int, int, int]
Palette = Dict[str, List[RGB]]


def _album_cover_url_from_item(item: Dict) -> Optional[str]:
    """Return the album cover URL from a track object, preferring the largest image."""
    album = item.get("album") or {}
    images = album.get("images") or []
    if not images:
        return None
    return images[0].get("url") or None


def get_album_cover_url(sp: spotipy.Spotify, track_id: Optional[str] = None) -> Optional[str]:
    """Return the album cover URL.

    - If ``track_id`` is provided, query ``/tracks/{id}``.
    - Otherwise, use the item currently playing via :func:`get_now_playing`.
    """
    if track_id:
        try:
            tr = sp.track(track_id)
            return _album_cover_url_from_item(tr)
        except Exception:
            # Fallback to now playing if the track lookup fails
            pass

    pb = get_now_playing(sp)
    if pb and pb.get("item"):
        return _album_cover_url_from_item(pb["item"])
    return None


def download_image_bytes(url: str, timeout: float = 10.0) -> Optional[bytes]:
    """Download the image into memory and return its bytes."""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.content
    except requests.RequestException:
        return None


def extract_album_colors_from_bytes(
    image_bytes: bytes,
    color_count: int = 5,
    quality: int = 1,
) -> Optional[Palette]:
    """Extract dominant color and palette using ColorThief from image bytes."""
    try:
        thief = ColorThief(BytesIO(image_bytes))
        dominant = thief.get_color(quality=quality)
        palette_list = thief.get_palette(color_count=color_count, quality=quality) or []
        # Normalize to tuples
        dom_t = (int(dominant[0]), int(dominant[1]), int(dominant[2]))
        pal_t = [tuple(map(int, p)) for p in palette_list]
        return {"dominant_color": [dom_t], "palette": pal_t}
    except Exception:
        return None


def get_current_album_colors(
    sp: spotipy.Spotify,
    color_count: int = 5,
    quality: int = 1,
) -> Optional[Palette]:
    """Get album colors for the currently playing track or ``None`` if nothing is playing."""
    url = get_album_cover_url(sp)
    if not url:
        return None
    img = download_image_bytes(url)
    if not img:
        return None
    return extract_album_colors_from_bytes(img, color_count=color_count, quality=quality)


def get_album_colors_for_schedule_item(
    sp: spotipy.Spotify,
    schedule_item: Dict,
    color_count: int = 5,
    quality: int = 1,
) -> Optional[Palette]:
    """Get album colors for a scheduler item from :func:`build_schedule`.

    Uses ``track_id`` if available.
    """
    track_id = schedule_item.get("track_id")
    url = get_album_cover_url(sp, track_id=track_id)
    if not url:
        return None
    img = download_image_bytes(url)
    if not img:
        return None
    return extract_album_colors_from_bytes(img, color_count=color_count, quality=quality)


if __name__ == "__main__":
    # Quick interactive example: requires environment variables and proper scope
    from .auth import create_spotify_client

    scope = "user-read-currently-playing user-read-playback-state"
    sp_client = create_spotify_client(scope=scope)
    colors = get_current_album_colors(sp_client)
    print(colors if colors else "Could not extract colors.")
