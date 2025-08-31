from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Section:
    name: str
    start: float
    end: float

def segment_by_density(beats: List[float], drum_onsets: List[float]) -> List[Section]:
    # Simple heuristic: every N bars alternates between verse and chorus
    bars = [beats[i] for i in range(0, len(beats), 4)]
    sections: List[Section] = []
    if not bars:
        return [Section("full", 0.0, beats[-1] if beats else 0.0)]
    size = max(1, len(bars) // 4)
    names = ["intro", "verse", "chorus", "bridge"]
    t0 = bars[0]
    for i, b in enumerate(bars[1:] + [bars[-1] + 4 * (bars[1]-bars[0] if len(bars) > 1 else 1.0)]):
        if i % size == 0:
            if i:
                sections[-1].end = b
            sections.append(Section(names[(len(sections)) % len(names)], b, b))
    if sections:
        sections[-1].end = bars[-1] if bars else sections[-1].start + 8.0
    return sections