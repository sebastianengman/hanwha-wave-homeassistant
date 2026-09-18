from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import aiohttp

from .const import CAMERAS_PATH, SNAPSHOT_PATH


class WaveApiError(Exception):
    """Raised when WAVE cannot be queried."""


@dataclass(slots=True)
class WaveCamera:
    camera_id: str
    name: str
    state: str | None = None
    snapshot_url: str | None = None


class WaveApi:
    def __init__(self, session: aiohttp.ClientSession, base_url: str, username: str, password: str) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._auth = aiohttp.BasicAuth(username, password)

    async def _request(self, path: str) -> Any:
        try:
            async with self._session.get(
                f"{self._base_url}{path}", auth=self._auth, timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status in (401, 403):
                    raise WaveApiError("Invalid WAVE credentials")
                if response.status >= 400:
                    raise WaveApiError(f"WAVE returned HTTP {response.status}")
                return await response.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError) as err:
            raise WaveApiError(str(err)) from err

    async def async_test(self) -> None:
        await self._request(CAMERAS_PATH)

    async def async_get_cameras(self) -> list[WaveCamera]:
        payload = await self._request(CAMERAS_PATH)
        items = payload.get("cameras", payload) if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise WaveApiError("Unexpected camera response from WAVE")
        result: list[WaveCamera] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            camera_id = str(item.get("id") or item.get("cameraId") or item.get("guid") or "")
            if not camera_id:
                continue
            name = str(item.get("name") or item.get("caption") or camera_id)
            result.append(WaveCamera(camera_id, name, item.get("state"), self.snapshot_url(camera_id)))
        return result

    def snapshot_url(self, camera_id: str) -> str:
        return f"{self._base_url}{SNAPSHOT_PATH.format(camera_id=camera_id)}"

    async def async_get_snapshot(self, camera_id: str) -> bytes:
        try:
            async with self._session.get(
                self.snapshot_url(camera_id), auth=self._auth, timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                if response.status >= 400:
                    raise WaveApiError(f"WAVE returned HTTP {response.status}")
                return await response.read()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise WaveApiError(str(err)) from err
