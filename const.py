"""Constants for the Creality Connect integration."""
from typing import Final

DOMAIN: Final = "creality_connect"

# Configuration
CONF_HOST: Final = "host"
CONF_PORT: Final = "port"
CONF_WS_PORT: Final = "ws_port"

# Default values
DEFAULT_PORT: Final = 9999
DEFAULT_WS_PORT: Final = 9999
DEFAULT_NAME: Final = "Creality K1 Max"

# Update intervals
SCAN_INTERVAL: Final = 1  # seconds

# Printer states
STATE_IDLE: Final = "idle"
STATE_PRINTING: Final = "printing"
STATE_PAUSED: Final = "paused"
STATE_COMPLETE: Final = "complete"
STATE_CANCELLED: Final = "cancelled"
STATE_ERROR: Final = "error"

# API endpoints
ENDPOINT_PRINTER_OBJECTS_QUERY: Final = "/printer/objects/query"
ENDPOINT_PRINTER_INFO: Final = "/printer/info"
ENDPOINT_SERVER_INFO: Final = "/server/info"

# WebSocket message types
WS_METHOD_NOTIFY: Final = "notify"
WS_METHOD_SET: Final = "set"

# Printer object keys
OBJ_PRINT_STATS: Final = "print_stats"
OBJ_TOOLHEAD: Final = "toolhead"
OBJ_EXTRUDER: Final = "extruder"
OBJ_HEATER_BED: Final = "heater_bed"
OBJ_FAN: Final = "fan"
OBJ_GCODE_MOVE: Final = "gcode_move"
OBJ_VIRTUAL_SDCARD: Final = "virtual_sdcard"

# Attribute keys
ATTR_STATE: Final = "state"
ATTR_FILENAME: Final = "filename"
ATTR_PROGRESS: Final = "progress"
ATTR_PRINT_DURATION: Final = "print_duration"
ATTR_TEMPERATURE: Final = "temperature"
ATTR_TARGET: Final = "target"
ATTR_POSITION: Final = "position"
ATTR_SPEED: Final = "speed"
ATTR_LAYER: Final = "layer"
ATTR_TOTAL_LAYER: Final = "total_layer"

# Fan types
FAN_MODEL: Final = "model"
FAN_SIDE: Final = "side"
FAN_CASE: Final = "case"

# Creality-specific parameter keys
PARAM_FAN: Final = "fan"  # Model fan (part cooling)
PARAM_AUXILIARY_FAN: Final = "auxiliaryFanPct"  # Side fan
PARAM_CASE_FAN: Final = "caseFanPct"  # Case/chamber fan
PARAM_LIGHT_SW: Final = "lightSw"  # LED light switch
PARAM_PAUSE: Final = "pause"
PARAM_STOP: Final = "stop"
PARAM_BED_TARGET_TEMP: Final = "bedTargetTemp"
PARAM_NOZZLE_TARGET_TEMP: Final = "nozzleTargetTemp"

