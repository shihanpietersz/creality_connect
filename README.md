# Creality Connect

[![GitHub Release](https://img.shields.io/github/release/shihanpietersz/creality_connect.svg?style=for-the-badge)](https://github.com/shihanpietersz/creality_connect/releases)
[![License](https://img.shields.io/github/license/shihanpietersz/creality_connect.svg?style=for-the-badge)](LICENSE)
[![hacs](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://hacs.xyz)

A complete Home Assistant custom integration for **Creality 3D printers** (K1, K1 Max, K1C, and more), featuring real-time monitoring, control, webcam streaming, and print management.

![Creality Connect](https://raw.githubusercontent.com/shihanpietersz/creality_connect/main/images/hero.png)

---

## ✨ Features

### 📊 Comprehensive Monitoring
- **Temperatures**: Nozzle and bed (current & target) with real-time updates
- **Print Progress**: Percentage, duration, remaining time (H:M:S format)
- **Position Tracking**: Live X, Y, Z coordinates
- **Speed Metrics**: Current speed and speed factor
- **Fan Monitoring**: Model, auxiliary, and case fan speeds
- **Layer Information**: Current and total layer count
- **Print State**: Idle, printing, paused, complete status

### 🎮 Full Control
- **LED Control**: Toggle printer lights on/off
- **Print Management**: Pause, resume, or cancel prints
- **Fan Speed Control**: Adjust all three fans (0-100%)
- **Temperature Control**: Set nozzle (0-300°C) and bed (0-120°C) targets
- **Homing**: Home all axes or individual X, Y, Z axes

### 📷 Live Media
- **Webcam Stream**: Real-time camera feed at 8080 port
- **Print Preview**: Current print thumbnail image

### ⚡ Real-time Updates
- Native Creality WebSocket protocol
- Instant sensor updates (no polling delay)
- Automatic reconnection on disconnect
- Efficient data handling

---

## 🚀 Installation

### HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Click on **Integrations**
3. Click the **⋮** menu (top-right) → **Custom repositories**
4. Add repository: `https://github.com/shihanpietersz/creality_connect`
5. Category: **Integration**
6. Click **Add**
7. Find **"Creality Connect"** and click **Download**
8. Restart Home Assistant
9. Go to **Settings** → **Devices & Services** → **Add Integration**
10. Search for **"Creality Connect"** and configure

### Manual Installation

1. Download the [latest release](https://github.com/shihanpietersz/creality_connect/releases)
2. Extract and copy the `creality_connect` folder to `/config/custom_components/`
3. Restart Home Assistant
4. Add via **Settings** → **Devices & Services** → **Add Integration**

📚 **Full Installation Guide**: [INSTALL.md](INSTALL.md)

---

## ⚙️ Configuration

During setup, you'll need:

| Field | Description | Default |
|-------|-------------|---------|
| **Host** | Printer IP address (e.g., `192.168.1.100`) | Required |
| **HTTP Port** | API port | `9999` |
| **WebSocket Port** | WebSocket port | `9999` |

**Finding your printer's IP**: Check your printer's LCD screen under Settings → Network

---

## 📱 Quick Example

### Dashboard Card
```yaml
type: entities
title: 3D Printer
entities:
  - sensor.creality_printer_state
  - sensor.creality_printer_print_progress
  - sensor.creality_printer_print_duration_formatted
  - sensor.creality_printer_print_time_remaining_formatted
  - sensor.creality_printer_nozzle_temperature
  - sensor.creality_printer_bed_temperature
  - switch.creality_printer_led_light
  - camera.creality_printer_camera
```

### Automation: Print Complete Notification
```yaml
automation:
  - alias: "Print Complete"
    trigger:
      - platform: state
        entity_id: sensor.creality_printer_state
        to: "complete"
    action:
      - service: notify.mobile_app
        data:
          title: "🎉 Print Complete!"
          message: "{{ states('sensor.creality_printer_current_file') }} finished"
```

More examples in [README.md](README.md)

---

## 🖥️ Supported Printers

Tested and confirmed working:

- ✅ Creality K1
- ✅ Creality K1 Max
- ✅ Creality K1C

Other Creality printers with Moonraker/Klipper should also work.

---

## 📊 Available Entities

### Sensors (20+)
- Temperatures (nozzle, bed - current & target)
- Print progress, duration, remaining time
- Position (X, Y, Z)
- Speed and speed factor
- Fan speeds (model, auxiliary, case)
- Layer info (current/total)
- Printer state and filename

### Controls
- **Switches**: LED light, pause/resume
- **Number Sliders**: Fan controls, target temperatures
- **Buttons**: Cancel print, home axes

### Media
- **Camera**: Live webcam stream
- **Image**: Print preview thumbnail

Full entity reference: [README.md#entity-reference](README.md#-entity-reference)

---

## 🐛 Troubleshooting

### Common Issues

**Cannot connect to printer:**
- Verify IP address is correct
- Check printer is powered on and connected
- Ensure port 9999 is accessible (firewall)

**Entities show "Unavailable":**
- Check WebSocket connection in logs
- Reload the integration
- Restart Home Assistant

**Webcam not working:**
- Test direct access: `http://YOUR_IP:8080/?action=stream`
- Verify webcam is enabled on printer

Full troubleshooting guide: [INSTALL.md#troubleshooting](INSTALL.md#-troubleshooting)

---

## 📚 Documentation

- **[README.md](README.md)** - Complete feature documentation and examples
- **[INSTALL.md](INSTALL.md)** - Detailed installation and troubleshooting guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step setup walkthrough

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/shihanpietersz/creality_connect/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shihanpietersz/creality_connect/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

---

## ⭐ Show Your Support

If you find this integration helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs or suggesting features
- 📝 Contributing improvements
- 💬 Sharing with the community

---

**Happy Printing! 🎉**

---

## 📸 Screenshots

_Coming soon - add your screenshots to `/images/` folder_

---

## 🗓️ Changelog

See [Releases](https://github.com/shihanpietersz/creality_connect/releases) for version history.

---

Made with ❤️ for the Home Assistant community


