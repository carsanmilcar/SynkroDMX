from __future__ import annotations
from typing import Dict, List, Tuple

def rgb_tuple(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def build_scene_rgb(fixtures: Dict[str, int], color_hex: str, dimmer: int = 255) -> Dict[int, int]:
    r, g, b = rgb_tuple(color_hex)
    updates: Dict[int, int] = {}
    for start in fixtures.values():
        updates[start + 0] = dimmer           # dimmer at ch 1
        updates[start + 1] = r                # R at ch 2
        updates[start + 2] = g                # G at ch 3
        updates[start + 3] = b                # B at ch 4
    return updates