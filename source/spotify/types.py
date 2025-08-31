
from __future__ import annotations

"""Type definitions for Spotify scheduling and polling."""

from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Tuple

RGB = Tuple[int, int, int]
ColorsDict = Dict[str, List[RGB]]  # {"dominant_color": (R,G,B), "palette": [(R,G,B), ...]}


@dataclass(frozen=True)
class ScheduleItem:
    """Minimal schedule block used to trigger scenes."""
    track_id: Optional[str]
    uri: Optional[str]
    title: str
    artist: str
    artist_id: Optional[str]
    genres: List[str]
    type: Literal["track", "episode", "unknown"]
    start_at_ms: int
    end_at_ms: int
    duration_ms: int
    context_uri: Optional[str]
    is_current: bool
    progress_ms: Optional[int]
    timestamp_ms: Optional[int]
    # Album cover colors
    colors: Optional[ColorsDict] = None


@dataclass
class PollerConfig:
    """Polling configuration with adaptive intervals near track boundaries."""
    interval_normal_s: float = 5.0
    interval_edge_s: float = 1.0
    edge_threshold_s: float = 5.0
    max_queue_items: int = 5
    save_last_schedule_json: Optional[str] = None  # Path to dump the last schedule
