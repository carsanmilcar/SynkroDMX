from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import pretty_midi


@dataclass
class MidiAnalysis:
    pm: pretty_midi.PrettyMIDI
    bpm: float
    tempo_times: List[float]
    tempo_bpms: List[float]
    time_signatures: List[Tuple[int, int]]
    beats: List[float]
    drum_onsets: List[float]


def load_midi(path: str | Path) -> MidiAnalysis:
    pm = pretty_midi.PrettyMIDI(str(path))
    tempo_times, tempo_bpms = pm.get_tempo_changes()
    # time signatures
    ts = [(ts.numerator, ts.denominator) for ts in getattr(pm, "time_signature_changes", [])]
    beats = pm.get_beats()
    # drums
    drum_inst = next((i for i in pm.instruments if i.is_drum), None)
    drum_onsets = sorted(n.start for n in (drum_inst.notes if drum_inst else []))
    bpm = float(tempo_bpms[0]) if len(tempo_bpms) else 120.0
    return MidiAnalysis(pm, bpm, tempo_times.tolist(), tempo_bpms.tolist(), ts, beats.tolist(), drum_onsets)