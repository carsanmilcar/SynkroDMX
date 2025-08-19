from __future__ import annotations
from typing import Callable

def flash(factory_setter: Callable[[dict[int, int]], None], restore: Callable[[], None], duration_ms: int = 100):
    # Placeholder: your scheduler should call factory_setter, wait, then restore
    factory_setter({})  # implement with your DMX runner
    restore()