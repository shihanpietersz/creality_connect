"""Switch platform for Creality Connect."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    PARAM_LIGHT_SW,
    PARAM_PAUSE,
)
from .coordinator import CrealityK1MaxCoordinator


@dataclass
class CrealityK1MaxSwitchEntityDescription(SwitchEntityDescription):
    """Describes Creality K1 Max switch entity."""

    value_fn: Callable[[dict[str, Any]], bool] | None = None
    turn_on_params: Callable[[], dict[str, Any]] | None = None
    turn_off_params: Callable[[], dict[str, Any]] | None = None


SWITCHES: tuple[CrealityK1MaxSwitchEntityDescription, ...] = (
    CrealityK1MaxSwitchEntityDescription(
        key="led_light",
        name="LED Light",
        icon="mdi:lightbulb",
        value_fn=lambda data: data.get("light_on", False),
        turn_on_params=lambda: {PARAM_LIGHT_SW: 1},
        turn_off_params=lambda: {PARAM_LIGHT_SW: 0},
    ),
    CrealityK1MaxSwitchEntityDescription(
        key="pause_resume",
        name="Pause/Resume Print",
        icon="mdi:pause",
        value_fn=lambda data: data.get("state") == "paused",
        turn_on_params=lambda: {PARAM_PAUSE: 1},  # Pause
        turn_off_params=lambda: {PARAM_PAUSE: 0},  # Resume
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max switch based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        CrealityK1MaxSwitch(coordinator, description, entry) for description in SWITCHES
    )


class CrealityK1MaxSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Creality K1 Max switch."""

    entity_description: CrealityK1MaxSwitchEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        description: CrealityK1MaxSwitchEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
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
        """Return true if the switch is on."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        if self.entity_description.turn_on_params:
            params = self.entity_description.turn_on_params()
            await self.coordinator.send_command(params)
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self.entity_description.turn_off_params:
            params = self.entity_description.turn_off_params()
            await self.coordinator.send_command(params)
            await self.coordinator.async_request_refresh()

