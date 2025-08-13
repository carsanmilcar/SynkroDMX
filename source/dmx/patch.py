from __future__ import annotations
from dataclasses import dataclass

@dataclass
class FixtureProfile:
    name: str
    channels: dict[str, int]  # e.g. {'dimmer':1, 'r':2, 'g':3, 'b':4}

RGB_DIMMER = FixtureProfile(
    name="rgb_dimmer",
    channels={"dimmer": 1, "r": 2, "g": 3, "b": 4},
)