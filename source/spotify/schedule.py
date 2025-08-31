from __future__ import annotations

"""Build playback schedules and enrich them with album colors."""

import time
from typing import Any, Dict, List, Optional
import spotipy

from .types import ScheduleItem
from .playback import get_now_playing, get_queue_safe, extract_artist_and_genres
from .album_colors import get_album_colors_for_schedule_item


def _now_ms() -> int:
    """Return current time in milliseconds."""
    return int(time.time() * 1000)


def _attach_colors(
    sp: spotipy.Spotify,
    block: Dict[str, Any],
    color_count: int,
    quality: int,
) -> None:
    """Enrich the block with ``colors``. Fail silently if they cannot be fetched."""
    try:
        colors = get_album_colors_for_schedule_item(
            sp,
            block,
            color_count=color_count,
            quality=quality,
        )
    except Exception:
        colors = None
    block["colors"] = colors


def build_schedule(
    sp: spotipy.Spotify,
    max_queue_items: int = 5,
    include_colors: bool = True,
    color_count: int = 5,
    quality: int = 1,
) -> List[Dict[str, Any]]:
    """Return ``[current_item, item_1, item_2, ...]`` with absolute times.

    Adds ``colors`` with the album cover palette when ``include_colors=True``.

    Note: fetching colors requires downloading the album image which may add
    latency. If you prefer to defer it, call with ``include_colors=False`` and
    use :func:`_attach_colors` later.
    """
    pb = get_now_playing(sp)
    if not pb or not pb.get("is_playing") or not pb.get("item"):
        return []

    item = pb["item"]
    item_type = pb.get("currently_playing_type") or item.get("type") or "unknown"
    duration_ms = int(item.get("duration_ms") or 0)
    progress_ms = int(pb.get("progress_ms") or 0)
    timestamp_ms = int(pb.get("timestamp") or _now_ms())
    context_uri = (pb.get("context") or {}).get("uri") if pb.get("context") else None

    artist_names, main_artist_id, genres = extract_artist_and_genres(sp, item, item_type)

    # Temporal anchor
    start_current = timestamp_ms - progress_ms
    end_current = start_current + duration_ms

    current_block: Dict[str, Any] = {
        "track_id": item.get("id"),
        "uri": item.get("uri"),
        "title": item.get("name"),
        "artist": artist_names,
        "artist_id": main_artist_id,
        "genres": genres,
        "type": item_type,
        "start_at_ms": start_current,
        "end_at_ms": end_current,
        "duration_ms": duration_ms,
        "context_uri": context_uri,
        "is_current": True,
        "progress_ms": progress_ms,
        "timestamp_ms": timestamp_ms,
    }

    if include_colors:
        _attach_colors(sp, current_block, color_count=color_count, quality=quality)

    schedule: List[Dict[str, Any]] = [current_block]

    # Next items in queue
    nxt_items = get_queue_safe(sp, max_queue_items)
    cursor = end_current
    for nxt in nxt_items:
        n_type = nxt.get("type") or "unknown"
        n_artist_names, n_main_artist_id, n_genres = extract_artist_and_genres(sp, nxt, n_type)
        n_dur = int(nxt.get("duration_ms") or 0)

        block: Dict[str, Any] = {
            "track_id": nxt.get("id"),
            "uri": nxt.get("uri"),
            "title": nxt.get("name"),
            "artist": n_artist_names,
            "artist_id": n_main_artist_id,
            "genres": n_genres,
            "type": n_type,
            "start_at_ms": cursor,
            "end_at_ms": cursor + n_dur,
            "duration_ms": n_dur,
            "context_uri": None,
            "is_current": False,
            "progress_ms": None,
            "timestamp_ms": None,
        }

        if include_colors:
            _attach_colors(sp, block, color_count=color_count, quality=quality)

        schedule.append(block)
        cursor += n_dur

    return schedule
