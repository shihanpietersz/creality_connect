"""Button platform for Creality Connect."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PARAM_STOP
from .coordinator import CrealityK1MaxCoordinator


@dataclass
class CrealityK1MaxButtonEntityDescription(ButtonEntityDescription):
    """Describes Creality K1 Max button entity."""

    press_params: Callable[[], dict[str, Any]] | None = None


BUTTONS: tuple[CrealityK1MaxButtonEntityDescription, ...] = (
    CrealityK1MaxButtonEntityDescription(
        key="cancel_print",
        name="Cancel Print",
        icon="mdi:stop",
        press_params=lambda: {PARAM_STOP: 1},
    ),
    CrealityK1MaxButtonEntityDescription(
        key="home_all",
        name="Home All Axes",
        icon="mdi:home",
        press_params=lambda: {"gcode": "G28"},
    ),
    CrealityK1MaxButtonEntityDescription(
        key="home_x",
        name="Home X Axis",
        icon="mdi:axis-x-arrow",
        press_params=lambda: {"gcode": "G28 X"},
    ),
    CrealityK1MaxButtonEntityDescription(
        key="home_y",
        name="Home Y Axis",
        icon="mdi:axis-y-arrow",
        press_params=lambda: {"gcode": "G28 Y"},
    ),
    CrealityK1MaxButtonEntityDescription(
        key="home_z",
        name="Home Z Axis",
        icon="mdi:axis-z-arrow",
        press_params=lambda: {"gcode": "G28 Z"},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max button based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        CrealityK1MaxButton(coordinator, description, entry) for description in BUTTONS
    )


class CrealityK1MaxButton(CoordinatorEntity, ButtonEntity):
    """Representation of a Creality K1 Max button."""

    entity_description: CrealityK1MaxButtonEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        description: CrealityK1MaxButtonEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Creality K1 Max",
            "manufacturer": "Creality",
            "model": "K1 Max",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        if self.entity_description.press_params:
            params = self.entity_description.press_params()
            await self.coordinator.send_command(params)
            await self.coordinator.async_request_refresh()

