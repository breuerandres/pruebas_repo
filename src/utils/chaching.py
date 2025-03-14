import asyncio
from typing import Dict, Optional
import json


class AsyncCache:
    def __init__(self):
        self._cache: Dict[str, str] = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: dict) -> None:
        value: str = json.dumps(value)
        async with self._lock:
            self._cache[key] = value

    async def get(self, key: str) -> Optional[dict]:
        async with self._lock:
            if key not in self._cache:
                return None
            value = json.loads(self._cache.get(key))
            return value
