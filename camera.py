"""Camera platform for Creality Connect."""
from __future__ import annotations

import asyncio
import logging

import aiohttp

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import CrealityK1MaxCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max camera based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([CrealityK1MaxCamera(coordinator, entry)])


class CrealityK1MaxCamera(Camera):
    """Representation of a Creality K1 Max camera (webcam stream)."""

    _attr_has_entity_name = True
    _attr_name = "Webcam"

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""
        super().__init__()
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_camera"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Creality K1 Max",
            "manufacturer": "Creality",
            "model": "K1 Max",
        }
        
        # Webcam stream URL (port 8080 for Creality K1 Max)
        self._stream_url = f"http://{coordinator.host}:8080/?action=stream"

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera stream."""
        # Get a snapshot instead of the stream
        snapshot_url = f"http://{self.coordinator.host}:8080/?action=snapshot"
        
        try:
            websession = async_get_clientsession(self.hass)
            async with websession.get(
                snapshot_url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    return await response.read()
                    
                _LOGGER.warning("Error getting camera snapshot: HTTP %s", response.status)
                return None
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to camera: %s", err)
            return None
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout getting camera snapshot")
            return None

    @property
    def is_on(self) -> bool:
        """Return true if camera is streaming."""
        return True

    @property
    def motion_detection_enabled(self) -> bool:
        """Return the camera motion detection status."""
        return False

    @property
    def brand(self) -> str:
        """Return the camera brand."""
        return "Creality"

    @property
    def model(self) -> str:
        """Return the camera model."""
        return "K1 Max Webcam"

