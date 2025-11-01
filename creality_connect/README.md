# Creality Connect - Home Assistant Integration

A complete Home Assistant custom integration for **Creality 3D printers** (K1, K1 Max, K1C, and more), featuring real-time monitoring, control, webcam streaming, and print management.

## ✨ Features

### 📊 **Sensors**
- **Temperatures**: Nozzle and bed (current & target)
- **Position**: X, Y, Z coordinates
- **Print Progress**: Percentage, duration, remaining time, filename, state
- **Speed**: Print speed and speed factor
- **Fan Speeds**: Model, auxiliary, and case fans
- **Layer Info**: Current layer and total layers

### 🔘 **Controls**

**Switches:**
- LED light on/off
- Pause/Resume print

**Numbers (Sliders):**
- Model fan speed (0-100%)
- Auxiliary fan speed (0-100%)
- Case fan speed (0-100%)
- Nozzle target temperature (0-300°C)
- Bed target temperature (0-120°C)

**Buttons:**
- Cancel print
- Home all axes
- Home X, Y, Z individually

### 📷 **Media**
- **Camera**: Live webcam stream
- **Image**: Current print preview thumbnail

### 🔄 **Real-time Updates**
- WebSocket connection for instant updates
- Automatic reconnection on disconnect
- Native Creality protocol support

---

## 📦 Installation

### Method 1: Manual Installation

1. **Copy the integration files:**
   ```bash
   cd /config
   mkdir -p custom_components
   cp -r creality_connect custom_components/
   ```

2. **Restart Home Assistant**

3. **Add the integration:**
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for **"Creality Connect"**
   - Enter your printer's IP address
   - Click **Submit**

### Method 2: HACS (Recommended)

_Coming soon - HACS submission in progress_

---

## 🔧 Configuration

### Required Information

- **Host (IP Address)**: Your printer's IP (e.g., `192.168.1.100`)
- **HTTP Port**: Default is `9999`
- **WebSocket Port**: Default is `9999`

### Finding Your Printer's IP

1. **From the Printer Screen:**
   - Navigate to **Settings** → **Network**
   - Note the IP address

2. **From Your Router:**
   - Check connected devices for "Creality" or "K1"

3. **Using Network Scanner:**
   - Use an app like "Fing" or "Advanced IP Scanner"

---

## 📱 Usage Examples

### Dashboard Card Example

```yaml
type: entities
title: 3D Printer
entities:
  - entity: sensor.creality_printer_state
  - entity: sensor.creality_printer_nozzle_temperature
  - entity: sensor.creality_printer_bed_temperature
  - entity: sensor.creality_printer_print_progress
  - entity: sensor.creality_printer_print_duration_formatted
  - entity: sensor.creality_printer_print_time_remaining_formatted
  - entity: switch.creality_printer_led_light
  - entity: switch.creality_printer_pause_resume
  - entity: camera.creality_printer_camera
  - entity: image.creality_printer_print_preview
```

### Automation Example: Print Complete Notification

```yaml
automation:
  - alias: "Notify when print completes"
    trigger:
      - platform: state
        entity_id: sensor.creality_printer_state
        to: "complete"
    action:
      - service: notify.mobile_app
        data:
          title: "Print Complete!"
          message: "Your 3D print has finished successfully."
```

### Automation Example: Temperature Alert

```yaml
automation:
  - alias: "Alert if nozzle overheats"
    trigger:
      - platform: numeric_state
        entity_id: sensor.creality_printer_nozzle_temperature
        above: 280
    action:
      - service: notify.mobile_app
        data:
          title: "Printer Alert"
          message: "Nozzle temperature too high!"
```

---

## 🛠️ Troubleshooting

### Connection Issues

**Problem**: Cannot connect to printer
**Solutions**:
1. Verify the IP address is correct
2. Ensure printer is powered on and connected to network
3. Check if port 9999 is accessible (firewall/router settings)
4. Try pinging the printer: `ping 192.168.1.100`

### WebSocket Not Connecting

**Problem**: Entities show "Unavailable"
**Solutions**:
1. Check Home Assistant logs: **Settings** → **System** → **Logs**
2. Restart the integration: **Settings** → **Devices & Services** → Reload
3. Verify WebSocket port (default 9999) is correct

### Webcam Not Showing

**Problem**: Camera entity shows black screen or error
**Solutions**:
1. Verify webcam is enabled on the printer
2. Check if stream is accessible: `http://YOUR_PRINTER_IP:8080/?action=stream`
3. Ensure port 8080 is accessible

### Sensors Not Updating

**Problem**: Values are stale or not changing
**Solutions**:
1. Check if printer is actually printing
2. Verify WebSocket connection in logs
3. Restart the integration
4. Check for firmware updates on the printer

---

## 🔌 Compatible Printers

This integration has been tested and confirmed working with:

- ✅ **Creality K1**
- ✅ **Creality K1 Max**
- ✅ **Creality K1C**

_Other Creality printers running Moonraker/Klipper should also work._

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone the repository
2. Copy to your HA test instance
3. Make your changes
4. Test thoroughly
5. Submit PR

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Built for the Home Assistant community
- Uses native Creality WebSocket protocol
- Inspired by the Moonraker integration

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/shihanpietersz/creality_connect/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shihanpietersz/creality_connect/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

---

## 📊 Entity Reference

### Sensors
| Entity ID | Description | Unit |
|-----------|-------------|------|
| `sensor.creality_printer_state` | Printer state (idle/printing/paused/complete) | - |
| `sensor.creality_printer_nozzle_temperature` | Current nozzle temperature | °C |
| `sensor.creality_printer_nozzle_target_temperature` | Target nozzle temperature | °C |
| `sensor.creality_printer_bed_temperature` | Current bed temperature | °C |
| `sensor.creality_printer_bed_target_temperature` | Target bed temperature | °C |
| `sensor.creality_printer_print_progress` | Print completion percentage | % |
| `sensor.creality_printer_print_duration` | Time elapsed | seconds |
| `sensor.creality_printer_print_duration_formatted` | Time elapsed (H:M:S) | - |
| `sensor.creality_printer_print_time_remaining` | Estimated time remaining | seconds |
| `sensor.creality_printer_print_time_remaining_formatted` | Time remaining (H:M:S) | - |
| `sensor.creality_printer_current_file` | Name of file being printed | - |
| `sensor.creality_printer_position_x` | X-axis position | mm |
| `sensor.creality_printer_position_y` | Y-axis position | mm |
| `sensor.creality_printer_position_z` | Z-axis position | mm |
| `sensor.creality_printer_print_speed` | Current print speed | mm/s |
| `sensor.creality_printer_speed_factor` | Speed multiplier | % |
| `sensor.creality_printer_model_fan_speed` | Model cooling fan speed | % |
| `sensor.creality_printer_auxiliary_fan_speed` | Auxiliary fan speed | % |
| `sensor.creality_printer_case_fan_speed` | Case fan speed | % |
| `sensor.creality_printer_current_layer` | Current layer number | - |
| `sensor.creality_printer_total_layers` | Total layers in print | - |

### Binary Sensors
| Entity ID | Description |
|-----------|-------------|
| `binary_sensor.creality_printer_printing` | Is printer currently printing? |
| `binary_sensor.creality_printer_paused` | Is print paused? |
| `binary_sensor.creality_printer_led` | Is LED light on? |

### Switches
| Entity ID | Description |
|-----------|-------------|
| `switch.creality_printer_led_light` | Toggle LED light |
| `switch.creality_printer_pause_resume` | Pause/Resume print |

### Numbers
| Entity ID | Description | Range |
|-----------|-------------|-------|
| `number.creality_printer_model_fan` | Control model fan speed | 0-100% |
| `number.creality_printer_auxiliary_fan` | Control auxiliary fan | 0-100% |
| `number.creality_printer_case_fan` | Control case fan | 0-100% |
| `number.creality_printer_nozzle_target` | Set nozzle target temp | 0-300°C |
| `number.creality_printer_bed_target` | Set bed target temp | 0-120°C |

### Buttons
| Entity ID | Description |
|-----------|-------------|
| `button.creality_printer_cancel_print` | Cancel current print |
| `button.creality_printer_home_all` | Home all axes |
| `button.creality_printer_home_x` | Home X axis |
| `button.creality_printer_home_y` | Home Y axis |
| `button.creality_printer_home_z` | Home Z axis |

### Media
| Entity ID | Description |
|-----------|-------------|
| `camera.creality_printer_camera` | Live webcam stream |
| `image.creality_printer_print_preview` | Print preview thumbnail |

---

**Happy Printing! 🎉**
