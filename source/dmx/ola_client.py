# source/dmx/ola_client.py
from __future__ import annotations
import glob
import os
import subprocess
import sys
from array import array

# 1) Discover Homebrew prefix or use fallback
try:
    prefix = subprocess.check_output(["brew", "--prefix"]).decode().strip()
except Exception:
    prefix = "/opt/homebrew"

# 2) Find OLA site-packages for python3.*
candidates = glob.glob(os.path.join(prefix, "opt", "ola", "libexec", "lib", "python3.*", "site-packages"))

# 3) Add them to sys.path
for p in candidates:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.append(p)

# 4) Import OLA
from ola.ClientWrapper import ClientWrapper


class OLAClient:
    """Basic wrapper to send DMX frames to a universe via OLA."""
    def __init__(self, universe: int = 1):
        self.universe = universe
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()

    def set_channels_once(self, updates: dict[int, int]) -> None:
        """Send a single frame with the specified channel updates."""
        levels = array("B", [0] * 512)
        for ch, val in updates.items():
            idx = ch - 1  # 1-based → 0-based
            levels[idx] = max(0, min(255, val))

        def dmx_sent(status):
            print("OK" if status.Succeeded() else "Fail")
            self.wrapper.Stop()

        self.client.SendDmx(self.universe, levels, dmx_sent)
        self.wrapper.Run()


if __name__ == "__main__":
    # Quick example: channel 1 to 120, channel 2 to 80
    ola = OLAClient(universe=1)
    ola.set_channels_once({1: 120, 2: 80})
