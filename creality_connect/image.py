"""Image platform for Creality Connect."""
from __future__ import annotations

import asyncio
from datetime import datetime
import logging

import aiohttp

from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CrealityK1MaxCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max image based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([CrealityK1MaxPrintPreview(coordinator, entry)])


class CrealityK1MaxPrintPreview(CoordinatorEntity, ImageEntity):
    """Representation of the current print preview thumbnail."""

    _attr_has_entity_name = True
    _attr_name = "Print Preview"

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the image entity."""
        super().__init__(coordinator)
        CoordinatorEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, coordinator.hass)
        
        self._attr_unique_id = f"{entry.entry_id}_print_preview"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Creality K1 Max",
            "manufacturer": "Creality",
            "model": "K1 Max",
        }
        
        self._last_image: bytes | None = None
        self._last_filename: str = ""

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        # Only fetch if a file is currently printing or loaded
        filename = self.coordinator.data.get("filename", "")
        
        if not filename:
            return self._last_image
            
        # Check if we need to fetch a new thumbnail
        if filename != self._last_filename:
            self._last_filename = filename
            await self._fetch_thumbnail()
            
        return self._last_image

    async def _fetch_thumbnail(self) -> None:
        """Fetch the print preview thumbnail."""
        # Creality stores current print image at this path
        # Add timestamp to bypass cache
        thumbnail_url = (
            f"http://{self.coordinator.host}/downloads/original/current_print_image.png"
            f"?date={datetime.now().isoformat()}"
        )
        
        try:
            websession = async_get_clientsession(self.hass)
            async with websession.get(
                thumbnail_url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    self._last_image = await response.read()
                    _LOGGER.debug("Fetched print preview thumbnail")
                else:
                    _LOGGER.warning(
                        "Error getting print preview: HTTP %s", response.status
                    )
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching print preview: %s", err)
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching print preview")

    @property
    def image_last_updated(self) -> datetime:
        """Return the timestamp of the last image update."""
        return datetime.now()

