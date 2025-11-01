"""Sensor platform for Creality Connect."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfLength,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CrealityK1MaxCoordinator


def _format_time(seconds: float | int | None) -> str:
    """Format time in seconds to H:M:S format."""
    if not seconds or seconds <= 0:
        return "0:00:00"
    
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    return f"{hours}:{minutes:02d}:{secs:02d}"


@dataclass
class CrealityK1MaxSensorEntityDescription(SensorEntityDescription):
    """Describes Creality K1 Max sensor entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None


SENSORS: tuple[CrealityK1MaxSensorEntityDescription, ...] = (
    CrealityK1MaxSensorEntityDescription(
        key="nozzle_temp",
        name="Nozzle Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("nozzle_temp"),
        icon="mdi:printer-3d-nozzle",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="nozzle_target",
        name="Nozzle Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("nozzle_target"),
        icon="mdi:printer-3d-nozzle",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="bed_temp",
        name="Bed Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("bed_temp"),
        icon="mdi:radiator",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="bed_target",
        name="Bed Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("bed_target"),
        icon="mdi:radiator",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="progress",
        name="Print Progress",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: round(data.get("progress", 0), 1),
        icon="mdi:progress-clock",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="print_duration",
        name="Print Duration",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        value_fn=lambda data: round(data.get("print_duration", 0)),
        icon="mdi:timer",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="print_duration_formatted",
        name="Print Duration (Formatted)",
        value_fn=lambda data: _format_time(data.get("print_duration", 0)),
        icon="mdi:timer",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="print_time_remaining",
        name="Print Time Remaining",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        value_fn=lambda data: round(data.get("print_time_remaining", 0)),
        icon="mdi:timer-sand",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="print_time_remaining_formatted",
        name="Print Time Remaining (Formatted)",
        value_fn=lambda data: _format_time(data.get("print_time_remaining", 0)),
        icon="mdi:timer-sand",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="filename",
        name="Current File",
        value_fn=lambda data: data.get("filename", "None"),
        icon="mdi:file",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="state",
        name="Printer State",
        value_fn=lambda data: data.get("state", "idle"),
        icon="mdi:printer-3d",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="position_x",
        name="Position X",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        value_fn=lambda data: data.get("position_x"),
        icon="mdi:axis-x-arrow",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="position_y",
        name="Position Y",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        value_fn=lambda data: data.get("position_y"),
        icon="mdi:axis-y-arrow",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="position_z",
        name="Position Z",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        value_fn=lambda data: data.get("position_z"),
        icon="mdi:axis-z-arrow",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="speed",
        name="Print Speed",
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=f"{UnitOfLength.MILLIMETERS}/s",
        value_fn=lambda data: data.get("speed"),
        icon="mdi:speedometer",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="speed_factor",
        name="Speed Factor",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("speed_factor"),
        icon="mdi:speedometer",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="fan_speed",
        name="Model Fan Speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: round(data.get("fan_speed", 0)),
        icon="mdi:fan",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="auxiliary_fan",
        name="Auxiliary Fan Speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: round(data.get("auxiliary_fan", 0)),
        icon="mdi:fan",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="case_fan",
        name="Case Fan Speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: round(data.get("case_fan", 0)),
        icon="mdi:fan",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="current_layer",
        name="Current Layer",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("current_layer", 0),
        icon="mdi:layers",
    ),
    CrealityK1MaxSensorEntityDescription(
        key="total_layers",
        name="Total Layers",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("total_layers", 0),
        icon="mdi:layers",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Creality K1 Max sensor based on a config entry."""
    coordinator: CrealityK1MaxCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        CrealityK1MaxSensor(coordinator, description, entry) for description in SENSORS
    )


class CrealityK1MaxSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Creality K1 Max sensor."""

    entity_description: CrealityK1MaxSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CrealityK1MaxCoordinator,
        description: CrealityK1MaxSensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
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
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None

