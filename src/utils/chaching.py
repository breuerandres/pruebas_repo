import asyncio
from typing import Dict, Optional


class AsyncCache:
    def __init__(self):
        self._cache: Dict[str, str] = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: str) -> None:
        async with self._lock:
            self._cache[key] = value

    async def get(self, key: str) -> Optional[str]:
        async with self._lock:
            return self._cache.get(key)
