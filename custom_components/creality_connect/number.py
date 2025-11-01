"""Number platform for Creality Connect."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    PARAM_AUXILIARY_FAN,
    PARAM_BED_TARGET_TEMP,
    PARAM_CASE_FAN,
    PARAM_FAN,
    PARAM_NOZZLE_TARGET_TEMP,
)
from .coordinator import CrealityK1MaxCoordinator


@dataclass
class CrealityK1MaxNumberEntityDescription(NumberEntityDescription):
    """Describes Creality K1 Max number entity."""

    value_fn: Callable[[dict[str, Any]], float] | None = None
    set_value_params: Callable[[float], dict[str, Any]] | None = None


NUMBERS: tuple[CrealityK1MaxNumberEntityDescription, ...] = (
    # Fan speeds
    CrealityK1MaxNumberEntityDescription(
        key="model_fan_speed",
        name="Model Fan Speed",
        icon="mdi:fan",
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=lambda data: data.get("fan_speed", 0),
        set_value_params=lambda value: {PARAM_FAN: int(value)},
    ),
    CrealityK1MaxNumberEntityDescription(
        key="auxiliary_fan_speed",
        name="Auxiliary Fan Speed",
        icon="mdi:fan",
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=lambda data: data.get("auxiliary_fan", 0),
        set_value_params=lambda value: {PARAM_AUXILIARY_FAN: int(value)},
    ),
    CrealityK1MaxNumberEntityDescription(
        key="case_fan_speed",
        name="Case Fan Speed",
        icon="mdi:fan",
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=lambda data: data.get("case_fan", 0),
        set_value_params=lambda value: {PARAM_CASE_FAN: int(value)},
    ),
    # Temperature setpoints
    CrealityK1MaxNumberEntityDescription(
        key="nozzle_target_temp",
        name="Nozzle Target Temperature",
        icon="mdi:printer-3d-nozzle",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=300,
        native_step=1,
        mode=NumberMode.BOX,
        value_fn=lambda data: data.get("nozzle_target", 0),
        set_value_params=lambda value: {PARAM_NOZZLE_TARGET_TEMP: int(value)},
    ),
    CrealityK1MaxNumberEntityDescription(
        key="bed_target_temp",
        name="Bed Target Temperature",
        icon="mdi:radiator",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=120,
        native_step=1,
        mode=NumberMode.BOX,
        value_fn=lambda data: data.get("bed_target", 0),
        set_value_params=lambda value: {PARAM_BED_TARGET_TEMP: int(value)},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max number based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        CrealityK1MaxNumber(coordinator, description, entry) for description in NUMBERS
    )


class CrealityK1MaxNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Creality K1 Max number entity."""

    entity_description: CrealityK1MaxNumberEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        description: CrealityK1MaxNumberEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
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
    def native_value(self) -> float:
        """Return the current value."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return 0

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        if self.entity_description.set_value_params:
            params = self.entity_description.set_value_params(value)
            await self.coordinator.send_command(params)
            await self.coordinator.async_request_refresh()

