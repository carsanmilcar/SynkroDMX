from __future__ import annotations
from typing import List, Tuple

def rescale_timeline(times: List[float], factor: float) -> List[float]:
    """Scale a list of timestamps by a factor (e.g., align MIDI to Spotify duration)."""
    return [t * factor for t in times]

def build_compas_grid(beats: List[float], numerador: int = 4) -> List[float]:
    """Return bar start times assuming fixed numerator (best-effort)."""
    return [beats[i] for i in range(0, len(beats), numerador)]