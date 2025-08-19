# source/dmx/ola_client.py
from __future__ import annotations
import glob
import os
import subprocess
import sys
from array import array

# 1) Descubrir prefix de Homebrew o usar fallback
try:
    prefix = subprocess.check_output(["brew", "--prefix"]).decode().strip()
except Exception:
    prefix = "/opt/homebrew"

# 2) Buscar site-packages de OLA para python3.*
candidates = glob.glob(os.path.join(prefix, "opt", "ola", "libexec", "lib", "python3.*", "site-packages"))

# 3) Añadirlos a sys.path
for p in candidates:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.append(p)

# 4) Importar OLA
from ola.ClientWrapper import ClientWrapper


class OLAClient:
    """Wrapper básico para enviar frames DMX a un universo vía OLA."""
    def __init__(self, universe: int = 1):
        self.universe = universe
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()

    def set_channels_once(self, updates: dict[int, int]) -> None:
        """Envía un frame único con los canales indicados actualizados."""
        levels = array("B", [0] * 512)
        for ch, val in updates.items():
            idx = ch - 1  # 1-based → 0-based
            levels[idx] = max(0, min(255, val))

        def dmx_sent(status):
            print("OK" if status.Succeeded() else "Fallo")
            self.wrapper.Stop()

        self.client.SendDmx(self.universe, levels, dmx_sent)
        self.wrapper.Run()


if __name__ == "__main__":
    # Ejemplo rápido: canal 1 a 120, canal 2 a 80
    ola = OLAClient(universe=1)
    ola.set_channels_once({1: 120, 2: 80})
