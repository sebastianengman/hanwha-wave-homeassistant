from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .api import WaveApi, WaveApiError
from .const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_SSL, CONF_USERNAME, DEFAULT_PORT, DOMAIN


async def _validate(hass: HomeAssistant, data: dict) -> None:
    scheme = "https" if data[CONF_SSL] else "http"
    api = WaveApi(hass.helpers.aiohttp_client.async_get_clientsession(), f"{scheme}://{data[CONF_HOST]}:{data[CONF_PORT]}", data[CONF_USERNAME], data[CONF_PASSWORD])
    await api.async_test()


class HanwhaWaveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            try:
                await _validate(self.hass, user_input)
            except WaveApiError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"Hanwha WAVE ({user_input[CONF_HOST]})", data=user_input)
        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.Coerce(int),
            vol.Required(CONF_SSL, default=False): bool,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
