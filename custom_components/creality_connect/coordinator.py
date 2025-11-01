"""Data update coordinator for Creality Connect."""
import asyncio
import json
import logging
from datetime import timedelta
from typing import Any

import aiohttp
import websockets
from websockets.client import WebSocketClientProtocol

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL, WS_METHOD_NOTIFY, WS_METHOD_SET

_LOGGER = logging.getLogger(__name__)


class CrealityK1MaxCoordinator(DataUpdateCoordinator):
    """Manage fetching Creality printer data."""

    def __init__(
        self, hass: HomeAssistant, host: str, port: int, ws_port: int
    ) -> None:
        """Initialize."""
        self.host = host
        self.port = port
        self.ws_port = ws_port
        self.http_base = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{ws_port}/websocket"
        
        self._websocket: WebSocketClientProtocol | None = None
        self._ws_task: asyncio.Task | None = None
        self._running = False
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via WebSocket."""
        if self.data:
            return self.data
        
        return {
            "state": "idle",
            "filename": "",
            "print_duration": 0,
            "print_time_remaining": 0,
            "total_duration": 0,
            "progress": 0,
            "nozzle_temp": 0,
            "nozzle_target": 0,
            "bed_temp": 0,
            "bed_target": 0,
            "position_x": 0,
            "position_y": 0,
            "position_z": 0,
            "speed": 0,
            "speed_factor": 100,
            "fan_speed": 0,
            "auxiliary_fan": 0,
            "case_fan": 0,
            "current_layer": 0,
            "total_layers": 0,
            "light_on": False,
        }

    def _process_printer_data(self, status: dict[str, Any]) -> dict[str, Any]:
        """Process printer data into structured format."""
        print_stats = status.get("print_stats", {})
        toolhead = status.get("toolhead", {})
        extruder = status.get("extruder", {})
        heater_bed = status.get("heater_bed", {})
        fan_data = status.get("fan", {})
        gcode_move = status.get("gcode_move", {})
        virtual_sdcard = status.get("virtual_sdcard", {})
        
        return {
            "state": print_stats.get("state", "idle"),
            "filename": print_stats.get("filename", ""),
            "print_duration": print_stats.get("print_duration", 0),
            "total_duration": print_stats.get("total_duration", 0),
            "progress": virtual_sdcard.get("progress", 0) * 100,
            "nozzle_temp": round(extruder.get("temperature", 0), 1),
            "nozzle_target": round(extruder.get("target", 0), 1),
            "bed_temp": round(heater_bed.get("temperature", 0), 1),
            "bed_target": round(heater_bed.get("target", 0), 1),
            "position_x": round(toolhead.get("position", [0, 0, 0, 0])[0], 2),
            "position_y": round(toolhead.get("position", [0, 0, 0, 0])[1], 2),
            "position_z": round(toolhead.get("position", [0, 0, 0, 0])[2], 2),
            "speed": round(gcode_move.get("speed", 0) / 60, 2),
            "speed_factor": round(gcode_move.get("speed_factor", 1.0) * 100, 0),
            "fan_speed": round(fan_data.get("speed", 0) * 100, 0),
            "auxiliary_fan": 0,
            "case_fan": 0,
            "current_layer": status.get("current_layer", 0),
            "total_layers": status.get("total_layers", 0),
            "light_on": False,
        }

    async def async_start_websocket(self) -> None:
        """Start WebSocket connection."""
        if self._running:
            return
            
        self._running = True
        self._ws_task = asyncio.create_task(self._websocket_loop())

    async def _websocket_loop(self) -> None:
        """WebSocket loop with auto-reconnect."""
        while self._running:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    self._websocket = websocket
                    _LOGGER.info("WebSocket connected to %s", self.ws_url)
                    
                    await self._subscribe_to_updates()
                    
                    async for message in websocket:
                        await self._handle_websocket_message(message)
                        
            except (websockets.exceptions.WebSocketException, OSError) as err:
                _LOGGER.warning("WebSocket disconnected: %s. Reconnecting...", err)
                self._websocket = None
                await asyncio.sleep(5)
                
            except Exception as err:
                _LOGGER.exception("Unexpected error in WebSocket loop: %s", err)
                await asyncio.sleep(5)

    async def _subscribe_to_updates(self) -> None:
        """Subscribe to printer updates."""
        if not self._websocket:
            return
            
        subscribe_msg = {
            "jsonrpc": "2.0",
            "method": "printer.objects.subscribe",
            "params": {
                "objects": {
                    "print_stats": None,
                    "toolhead": None,
                    "extruder": None,
                    "heater_bed": None,
                    "fan": None,
                    "gcode_move": None,
                    "virtual_sdcard": None,
                }
            },
            "id": 1,
        }
        
        try:
            await self._websocket.send(json.dumps(subscribe_msg))
        except Exception as err:
            _LOGGER.error("Failed to subscribe to updates: %s", err)

    async def _handle_websocket_message(self, message: str) -> None:
        """Handle WebSocket messages."""
        try:
            data = json.loads(message)
            
            if "nozzleTemp" in data or "bedTemp0" in data or "TotalLayer" in data:
                _LOGGER.debug("Received Creality format data")
                updated_data = {}
                
                if "nozzleTemp" in data:
                    updated_data["nozzle_temp"] = round(float(data["nozzleTemp"]), 1)
                if "bedTemp0" in data:
                    updated_data["bed_temp"] = round(float(data["bedTemp0"]), 1)
                if "targetNozzleTemp" in data:
                    updated_data["nozzle_target"] = round(float(data["targetNozzleTemp"]), 1)
                if "targetBedTemp0" in data:
                    updated_data["bed_target"] = round(float(data["targetBedTemp0"]), 1)
                
                if "printProgress" in data:
                    updated_data["progress"] = round(float(data["printProgress"]), 1)
                if "printJobTime" in data:
                    updated_data["print_duration"] = int(data["printJobTime"])
                if "printLeftTime" in data:
                    updated_data["print_time_remaining"] = int(data["printLeftTime"])
                    if "printJobTime" in data:
                        updated_data["total_duration"] = int(data["printJobTime"]) + int(data["printLeftTime"])
                
                if "printFileName" in data:
                    updated_data["filename"] = str(data["printFileName"]).split("/")[-1]
                if "state" in data or "deviceState" in data:
                    state_code = data.get("deviceState", data.get("state", 0))
                    state_map = {0: "idle", 1: "printing", 2: "paused", 3: "complete"}
                    updated_data["state"] = state_map.get(state_code, "idle")
                
                if "curPosition" in data:
                    pos_str = data["curPosition"]
                    x_match = pos_str.split("X:")[1].split()[0] if "X:" in pos_str else "0"
                    y_match = pos_str.split("Y:")[1].split()[0] if "Y:" in pos_str else "0"
                    z_match = pos_str.split("Z:")[1].split()[0] if "Z:" in pos_str else "0"
                    updated_data["position_x"] = round(float(x_match), 2)
                    updated_data["position_y"] = round(float(y_match), 2)
                    updated_data["position_z"] = round(float(z_match), 2)
                
                if "realTimeSpeed" in data:
                    updated_data["speed"] = round(float(data["realTimeSpeed"]), 2)
                if "curFeedratePct" in data:
                    updated_data["speed_factor"] = round(float(data["curFeedratePct"]), 0)
                
                if "layer" in data:
                    updated_data["current_layer"] = int(data["layer"])
                if "TotalLayer" in data:
                    updated_data["total_layers"] = int(data["TotalLayer"])
                
                if self.data:
                    self.async_set_updated_data({**self.data, **updated_data})
                else:
                    self.async_set_updated_data(updated_data)
                    
                return
            
            if data.get("method") == WS_METHOD_NOTIFY:
                params = data.get("params", [{}])
                if params:
                    status = params[0]
                    
                    if self.data:
                        updated_data = self._process_printer_data(status)
                        self.async_set_updated_data({**self.data, **updated_data})
                        
        except json.JSONDecodeError:
            _LOGGER.warning("Failed to decode WebSocket message: %s", message)
        except Exception as err:
            _LOGGER.exception("Error handling WebSocket message: %s", err)

    async def send_command(self, params: dict[str, Any]) -> bool:
        """Send command to printer."""
        if not self._websocket:
            _LOGGER.error("WebSocket not connected")
            return False
            
        try:
            msg = {
                "method": WS_METHOD_SET,
                "params": params,
            }
            
            await self._websocket.send(json.dumps(msg))
            _LOGGER.debug("Sent command: %s", msg)
            return True
            
        except Exception as err:
            _LOGGER.error("Failed to send command: %s", err)
            return False

    async def async_shutdown(self) -> None:
        """Shutdown WebSocket connection."""
        self._running = False
        
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
            
        if self._ws_task:
            self._ws_task.cancel()
            try:
                await self._ws_task
            except asyncio.CancelledError:
                pass
            self._ws_task = None

