
"""Spotify module for SynkroDMX providing a minimal playback scheduler."""
from .types import ScheduleItem, PollerConfig
from .auth import create_spotify_client
from .schedule import build_schedule
from .poller import SchedulerPoller
from .album_colors import (
    get_album_cover_url,
    download_image_bytes,
    extract_album_colors_from_bytes,
    get_current_album_colors,
    get_album_colors_for_schedule_item,
)
__all__ = [
    "ScheduleItem",
    "PollerConfig",
    "create_spotify_client",
    "build_schedule",
    "SchedulerPoller",
    "get_album_cover_url",
    "download_image_bytes",
    "extract_album_colors_from_bytes",
    "get_current_album_colors",
    "get_album_colors_for_schedule_item",
]
