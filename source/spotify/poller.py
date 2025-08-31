
from __future__ import annotations

"""Polling loop utilities for monitoring Spotify playback schedules."""

import json
import time
from typing import Any, Callable, Dict, List, Optional
import spotipy

try:
    from spotipy.exceptions import SpotifyException
except Exception:  # pragma: no cover
    SpotifyException = Exception

from .types import PollerConfig
from .schedule import build_schedule

OnScheduleChange = Callable[[List[Dict[str, Any]]], None]
OnError = Callable[[Exception], None]

class SchedulerPoller:
    """Minimal polling loop with backoff, change detection, and callbacks."""

    def __init__(
        self,
        sp: spotipy.Spotify,
        cfg: Optional[PollerConfig] = None,
        on_change: Optional[OnScheduleChange] = None,
        on_error: Optional[OnError] = None,
    ) -> None:
        self.sp = sp
        self.cfg = cfg or PollerConfig()
        self.on_change = on_change
        self.on_error = on_error
        self.last_track_id: Optional[str] = None
        self.last_start_ms: Optional[int] = None

    def _sleep_adaptive(self, schedule: List[Dict[str, Any]]) -> None:
        """Sleep faster near a track change boundary."""
        if not schedule:
            time.sleep(self.cfg.interval_normal_s)
            return
        cur = schedule[0]
        now_ms = int(time.time() * 1000)
        remaining_ms = max(0, int(cur.get("end_at_ms", 0)) - now_ms)
        if remaining_ms <= int(self.cfg.edge_threshold_s * 1000):
            time.sleep(self.cfg.interval_edge_s)
        else:
            time.sleep(self.cfg.interval_normal_s)

    def _handle_schedule(self, schedule: List[Dict[str, Any]]) -> None:
        """Invoke the change callback on new track or seek and optionally dump JSON."""
        changed = False
        if schedule:
            cur = schedule[0]
            track_id = cur.get("track_id")
            start_ms = cur.get("start_at_ms")
            changed = track_id != self.last_track_id or start_ms != self.last_start_ms
            if changed:
                self.last_track_id = track_id
                self.last_start_ms = start_ms

        if changed and self.on_change:
            self.on_change(schedule)

        if self.cfg.save_last_schedule_json:
            try:
                with open(self.cfg.save_last_schedule_json, "w", encoding="utf-8") as fh:
                    json.dump(schedule, fh, ensure_ascii=False, indent=2)
            except Exception as e:
                if self.on_error:
                    self.on_error(e)

    def run_forever(self) -> None:
        backoff_s = 1.0
        while True:
            try:
                schedule = build_schedule(self.sp, max_queue_items=self.cfg.max_queue_items)
                self._handle_schedule(schedule)
                backoff_s = 1.0
                self._sleep_adaptive(schedule)
            except SpotifyException as e:
                # Rate limiting
                retry_after = None
                try:
                    retry_after = int(e.http_headers.get("Retry-After")) if hasattr(e, "http_headers") else None
                except Exception:
                    retry_after = None
                wait = float(retry_after or backoff_s)
                if self.on_error:
                    self.on_error(e)
                time.sleep(wait)
                backoff_s = min(backoff_s * 2, 30.0)
            except KeyboardInterrupt:
                break
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
                time.sleep(backoff_s)
                backoff_s = min(backoff_s * 2, 30.0)
