from __future__ import annotations

from datetime import timedelta
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WaveApi, WaveApiError, WaveCamera
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    api: WaveApi = hass.data[DOMAIN][entry.entry_id]

    async def update() -> list[WaveCamera]:
        try:
            return await api.async_get_cameras()
        except WaveApiError as err:
            raise UpdateFailed(str(err)) from err

    coordinator = DataUpdateCoordinator(hass, "Hanwha WAVE", update_method=update, update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL))
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([WaveCameraEntity(api, coordinator, camera) for camera in coordinator.data])


class WaveCameraEntity(Camera):
    _attr_has_entity_name = True
    _attr_supported_features = CameraEntityFeature.ON_OFF

    def __init__(self, api: WaveApi, coordinator: DataUpdateCoordinator, camera: WaveCamera) -> None:
        super().__init__()
        self._api = api
        self.coordinator = coordinator
        self._camera = camera
        self._attr_unique_id = f"hanwha_wave_{camera.camera_id}"
        self._attr_name = camera.name
        self._attr_brand = "Hanwha"

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self):
        return {"wave_camera_id": self._camera.camera_id, "wave_state": self._camera.state}

    async def async_camera_image(self, width=None, height=None) -> bytes | None:
        try:
            return await self._api.async_get_snapshot(self._camera.camera_id)
        except WaveApiError:
            return None
