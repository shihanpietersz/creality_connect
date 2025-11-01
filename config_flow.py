"""Config flow for Creality Connect integration."""
import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import CONF_PORT, CONF_WS_PORT, DEFAULT_NAME, DEFAULT_PORT, DEFAULT_WS_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST]
    port = data.get(CONF_PORT, DEFAULT_PORT)
    
    _LOGGER.debug(f"Attempting to connect to {host}:{port}")
    
    async with aiohttp.ClientSession() as session:
        endpoints_to_try = [
            f"http://{host}:{port}/",
            f"http://{host}:{port}/server/info",
            f"http://{host}:{port}/printer/info",
        ]
        
        for endpoint in endpoints_to_try:
            try:
                _LOGGER.debug(f"Testing endpoint: {endpoint}")
                async with session.get(
                    endpoint,
                    timeout=aiohttp.ClientTimeout(total=5),
                    ssl=False,
                ) as response:
                    _LOGGER.info(f"Printer responded with HTTP {response.status} - connection valid")
                    return {"title": f"Creality Printer ({host})"}
                    
            except asyncio.TimeoutError:
                _LOGGER.debug(f"Timeout on {endpoint}")
                continue
            except aiohttp.ClientError as err:
                _LOGGER.debug(f"Error on {endpoint}: {err}")
                continue
            except Exception as err:
                _LOGGER.debug(f"Unexpected error on {endpoint}: {err}")
                continue
        
        _LOGGER.error(f"Cannot reach printer at {host}:{port}")
        raise ConnectionError(
            f"Cannot connect to printer at {host}:{port}. "
            "Please check the IP address and ensure the printer is online."
        )


class CrealityK1MaxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Creality Connect."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                # Check if already configured
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)
                
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                vol.Optional(CONF_WS_PORT, default=DEFAULT_WS_PORT): cv.port,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_data)

