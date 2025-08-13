import json
import time
from pathlib import Path

import click
from rich.console import Console

from source.audio.midi_loader import load_midi
from source.audio.spotify_sync import wait_for_track_start
from source.dmx.ola_client import OLAClient
from source.scenes.generators import build_scene_rgb

console = Console()

@click.group()
def cli():
    pass

@cli.command()
@click.option("--midi", type=click.Path(exists=True), required=True)
def prepare(midi):
    ma = load_midi(midi)
    out = {
        "bpm": ma.bpm,
        "drum_onsets": ma.drum_onsets[:50],
    }
    Path("assets/show_preview.json").write_text(json.dumps(out, indent=2))
    console.print("[green]Prepared show preview -> assets/show_preview.json[/green]")

@cli.command()
@click.option("--track", required=True, help="Spotify track id")
@click.option("--midi", type=click.Path(exists=True), required=True)
def run(track, midi):
    ma = load_midi(midi)
    console.print(f"[cyan]Loaded MIDI. Estimated BPM: {ma.bpm:.2f}[/cyan]")
    console.print("[yellow]Waiting for Spotify track start...[/yellow]")
    # NOTE: Initialize Spotipy client and wait here if desired
    t0 = time.perf_counter()  # placeholder if you start manually
    ola = OLAClient(universe=1)
    fixtures = {"PAR_BACK_1": 1, "PAR_BACK_2": 5}
    updates = build_scene_rgb(fixtures, "#0000FF", dimmer=200)
    ola.set_channels(updates)
    ola.send_now()
    console.print("[green]Scene sent to OLA.[/green]")

if __name__ == "__main__":
    cli()