"""Binary sensor platform for Creality Connect."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CrealityK1MaxCoordinator


@dataclass
class CrealityK1MaxBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Creality K1 Max binary sensor entity."""

    value_fn: Callable[[dict[str, Any]], bool] | None = None


BINARY_SENSORS: tuple[CrealityK1MaxBinarySensorEntityDescription, ...] = (
    CrealityK1MaxBinarySensorEntityDescription(
        key="is_printing",
        name="Printing",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda data: data.get("state") == "printing",
        icon="mdi:printer-3d",
    ),
    CrealityK1MaxBinarySensorEntityDescription(
        key="is_paused",
        name="Paused",
        value_fn=lambda data: data.get("state") == "paused",
        icon="mdi:pause",
    ),
    CrealityK1MaxBinarySensorEntityDescription(
        key="light_on",
        name="LED Light",
        device_class=BinarySensorDeviceClass.LIGHT,
        value_fn=lambda data: data.get("light_on", False),
        icon="mdi:lightbulb",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max binary sensor based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        CrealityK1MaxBinarySensor(coordinator, description, entry)
        for description in BINARY_SENSORS
    )


class CrealityK1MaxBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Creality K1 Max binary sensor."""

    entity_description: CrealityK1MaxBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        description: CrealityK1MaxBinarySensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Creality K1 Max",
            "manufacturer": "Creality",
            "model": "K1 Max",
        }

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return False

