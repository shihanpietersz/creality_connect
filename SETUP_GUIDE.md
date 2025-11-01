# Creality K1 Max Home Assistant Integration - Setup Guide

## 🎉 **Your Integration is Ready!**

I've created a **complete Home Assistant custom integration** for your Creality K1 Max printer with all the features from your React app and more!

---

## 📁 **What's Included**

### Core Files
```
creality_k1_max/
├── __init__.py          ✅ Main integration setup with WebSocket
├── manifest.json        ✅ Integration metadata
├── config_flow.py       ✅ Easy setup UI
├── const.py            ✅ Constants and configuration
├── coordinator.py      ✅ Data coordinator with WebSocket support
├── strings.json        ✅ UI translations
```

### Platform Files (Entities)
```
├── sensor.py           ✅ 18 sensors (temps, position, progress, fans, layers)
├── binary_sensor.py    ✅ 3 binary sensors (printing, paused, light)
├── switch.py           ✅ 2 switches (LED light, pause/resume)
├── number.py           ✅ 5 number controls (fan speeds, temps)
├── button.py           ✅ 5 buttons (cancel, home axes)
├── camera.py           ✅ Webcam streaming
├── image.py            ✅ Print preview thumbnail
```

### Documentation
```
├── README.md           ✅ Complete feature documentation
├── INSTALL.md          ✅ Step-by-step installation guide
└── SETUP_GUIDE.md      ✅ This file
```

---

## 🚀 **Quick Start (3 Steps)**

### Step 1: Copy to Home Assistant

**Copy the entire `creality_k1_max` folder to:**
```
/config/custom_components/creality_k1_max/
```

**Methods:**
- **SSH/Terminal**: `cp -r creality_k1_max /config/custom_components/`
- **Samba/File Share**: Drag and drop the folder
- **VS Code**: Use the Home Assistant File Editor addon

### Step 2: Restart Home Assistant

**Settings** → **System** → **Restart**

### Step 3: Add Integration

1. **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search **"Creality K1 Max"**
4. Enter printer IP: `192.168.3.62` (or your printer's IP)
5. Ports: `9999` (HTTP), `9999` (WebSocket)
6. Click **Submit**

✅ **Done!** Your printer is now integrated.

---

## 🎯 **What You Get**

### 📊 All Your App Features

| Feature | Status | Details |
|---------|--------|---------|
| **Real-time Updates** | ✅ | WebSocket connection (same as your app) |
| **Temperature Monitoring** | ✅ | Nozzle & bed (current + target) |
| **Print Progress** | ✅ | Percentage, duration, filename, state |
| **Position Tracking** | ✅ | X, Y, Z coordinates |
| **Fan Control** | ✅ | Model, side, case fans (0-100%) |
| **LED Light Control** | ✅ | On/Off switch |
| **Webcam Stream** | ✅ | Live camera feed (port 8080) |
| **Print Preview** | ✅ | Current print thumbnail |
| **Layer Info** | ✅ | Current/total layers |
| **Print Control** | ✅ | Pause, resume, cancel |
| **Homing** | ✅ | Home all or individual axes |

### 🆕 Bonus Features (Not in Your App)

- **Binary Sensors**: Easy automation triggers (is_printing, is_paused)
- **History Tracking**: All sensor data stored in Home Assistant database
- **Graphs**: Beautiful graphs for temps, progress, etc.
- **Notifications**: Push notifications when prints complete/fail
- **Voice Control**: "Alexa, turn off the printer light"
- **Complex Automations**: Temperature-based fan control, etc.

---

## 📱 **Example Dashboard**

Once set up, create a dashboard like this:

```yaml
type: vertical-stack
cards:
  # Status Card
  - type: entities
    title: Printer Status
    entities:
      - sensor.creality_k1_max_printer_state
      - sensor.creality_k1_max_current_file
      - sensor.creality_k1_max_print_progress
      - sensor.creality_k1_max_print_duration
  
  # Webcam
  - type: picture-entity
    entity: camera.creality_k1_max_webcam
    camera_image: camera.creality_k1_max_webcam
  
  # Temperatures
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.creality_k1_max_nozzle_temperature
        min: 0
        max: 300
      - type: gauge
        entity: sensor.creality_k1_max_bed_temperature
        min: 0
        max: 120
  
  # Controls
  - type: entities
    title: Controls
    entities:
      - switch.creality_k1_max_led_light
      - number.creality_k1_max_model_fan_speed
      - number.creality_k1_max_case_fan_speed
      - button.creality_k1_max_cancel_print
```

---

## 🤖 **Example Automations**

### Auto LED Control
```yaml
automation:
  - alias: "Turn on LED when printing starts"
    trigger:
      - platform: state
        entity_id: binary_sensor.creality_k1_max_printing
        to: "on"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.creality_k1_max_led_light
```

### Print Complete Notification
```yaml
automation:
  - alias: "Notify when print completes"
    trigger:
      - platform: state
        entity_id: sensor.creality_k1_max_printer_state
        to: "complete"
    action:
      - service: notify.mobile_app
        data:
          message: "Print finished: {{ states('sensor.creality_k1_max_current_file') }}"
```

### Smart Fan Control
```yaml
automation:
  - alias: "Adjust case fan based on bed temp"
    trigger:
      - platform: numeric_state
        entity_id: sensor.creality_k1_max_bed_temperature
        above: 60
    action:
      - service: number.set_value
        target:
          entity_id: number.creality_k1_max_case_fan_speed
        data:
          value: 80
```

---

## 🔧 **Technical Details**

### Protocol Support

✅ **Creality Native WebSocket Protocol** (same as your app):
```json
{
  "method": "set",
  "params": {
    "fan": 80,
    "lightSw": 1
  }
}
```

✅ **Moonraker JSON-RPC** (for subscriptions):
```json
{
  "jsonrpc": "2.0",
  "method": "printer.objects.subscribe",
  "params": { "objects": {...} },
  "id": 1
}
```

### Network Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 9999 | HTTP | Moonraker REST API |
| 9999 | WebSocket | Real-time updates |
| 8080 | HTTP | Webcam stream |

### Update Frequency

- **WebSocket**: Real-time (instant updates)
- **HTTP Polling**: 1 second (fallback if WS disconnects)
- **Camera**: On demand
- **Image**: When filename changes

---

## 🎓 **Learn More**

- **Full Documentation**: See [README.md](README.md)
- **Installation Help**: See [INSTALL.md](INSTALL.md)
- **Troubleshooting**: See [README.md#troubleshooting](README.md#-troubleshooting)

---

## 💡 **Tips**

1. **Add to your main dashboard** for quick access
2. **Create automations** for hands-free operation
3. **Enable notifications** to never miss a print completion
4. **Use graphs** to track temperature trends
5. **Set up voice control** with Google/Alexa
6. **Create scenes** for different print profiles (PLA, ABS, etc.)

---

## 🆘 **Need Help?**

1. Check the [troubleshooting guide](README.md#-troubleshooting)
2. Enable debug logging:
   ```yaml
   logger:
     logs:
       custom_components.creality_k1_max: debug
   ```
3. Check Home Assistant logs: **Settings** → **System** → **Logs**
4. Open an issue on GitHub (when published)

---

## 🎊 **Enjoy Your Smart 3D Printer!**

Your Creality K1 Max is now fully integrated with Home Assistant. You have:

- ✅ Real-time monitoring
- ✅ Full control (fans, lights, temps)
- ✅ Webcam streaming
- ✅ Print management
- ✅ Automation capabilities
- ✅ Voice control ready
- ✅ Beautiful dashboards

**Happy Printing! 🖨️✨**

