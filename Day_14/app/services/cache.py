from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any


class TTLCache:
    """Small in-process LRU cache with a time-to-live."""

    def __init__(self, max_entries: int = 128, ttl_seconds: int = 60) -> None:
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self._items: OrderedDict[str, tuple[float, Any]] = OrderedDict()

    def get(self, key: str) -> Any | None:
        item = self._items.get(key)
        if item is None:
            return None
        expires_at, value = item
        if expires_at <= time.monotonic():
            del self._items[key]
            return None
        self._items.move_to_end(key)
        return value

    def set(self, key: str, value: Any) -> None:
        self._items[key] = (time.monotonic() + self.ttl_seconds, value)
        self._items.move_to_end(key)
        while len(self._items) > self.max_entries:
            self._items.popitem(last=False)

    def clear(self) -> None:
        self._items.clear()
