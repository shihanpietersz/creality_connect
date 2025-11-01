# Installation Guide - Creality Connect

Complete step-by-step installation guide for the Creality Connect Home Assistant integration.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ Home Assistant (2023.1 or later)
- ✅ Creality 3D printer (K1, K1 Max, K1C, etc.) with Moonraker/Klipper
- ✅ Printer connected to your local network
- ✅ Printer's IP address

---

## 🚀 Installation Methods

### Method 1: Manual Installation (Recommended for first-time users)

#### Step 1: Download the Integration

**Option A: Download from GitHub Releases**
1. Go to [Releases](https://github.com/shihanpietersz/creality_connect/releases)
2. Download the latest `creality_connect.zip`
3. Extract the ZIP file

**Option B: Clone the Repository**
```bash
git clone https://github.com/shihanpietersz/creality_connect.git
```

#### Step 2: Copy Files to Home Assistant

**Using SSH/Terminal:**
```bash
# Connect to your Home Assistant instance
ssh root@homeassistant.local

# Navigate to config directory
cd /config

# Create custom_components if it doesn't exist
mkdir -p custom_components

# Copy the integration
cp -r /path/to/creality_connect custom_components/

# Verify the files are in place
ls -la custom_components/creality_connect/
```

**Using Samba/File Share:**
1. Connect to your Home Assistant via network share
2. Navigate to `config/custom_components/`
3. Create a folder called `creality_connect`
4. Copy all files from the integration into this folder

**Expected Directory Structure:**
```
/config/custom_components/creality_connect/
├── __init__.py
├── manifest.json
├── const.py
├── coordinator.py
├── config_flow.py
├── strings.json
├── sensor.py
├── binary_sensor.py
├── switch.py
├── number.py
├── button.py
├── camera.py
└── image.py
```

#### Step 3: Restart Home Assistant

**Via UI:**
1. Go to **Settings** → **System**
2. Click **Restart** (top-right corner)
3. Wait for Home Assistant to come back online

**Via SSH:**
```bash
ha core restart
```

#### Step 4: Add the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom-right)
3. Search for **"Creality Connect"**
4. Click on it to start setup

#### Step 5: Configure the Integration

You'll be prompted to enter:

| Field | Description | Example | Default |
|-------|-------------|---------|---------|
| **Host** | Printer's IP address | `192.168.1.100` | - |
| **HTTP Port** | HTTP/API port | `9999` | `9999` |
| **WebSocket Port** | WebSocket port | `9999` | `9999` |

**How to Find Your Printer's IP:**

1. **From Printer Screen:**
   - Touch **Settings** → **Network** → **IP Address**

2. **From Router:**
   - Log into your router admin panel
   - Look for "Creality" or "K1" in connected devices

3. **Using Network Scanner:**
   - Install "Fing" app (mobile) or "Advanced IP Scanner" (PC)
   - Scan your network for new devices
   - Look for Creality printer

#### Step 6: Verify Installation

After setup, you should see:

- ✅ A new device: **"Creality Printer (192.168.x.x)"**
- ✅ Multiple entities (sensors, switches, etc.)
- ✅ All entities showing as "Available" (not "Unavailable")

---

### Method 2: HACS Installation (Coming Soon)

_HACS submission is in progress. Once approved, installation will be even simpler:_

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click **Explore & Download Repositories**
4. Search for **"Creality Connect"**
5. Click **Download**
6. Restart Home Assistant
7. Add the integration via **Settings** → **Devices & Services**

---

## 🔍 Finding Your Printer's IP Address

### Method 1: Printer LCD Screen
1. On your printer, navigate to **Settings**
2. Select **Network** or **Wi-Fi**
3. The IP address will be displayed (e.g., `192.168.1.100`)

### Method 2: Router Admin Panel
1. Log into your router (usually `192.168.1.1` or `192.168.0.1`)
2. Go to **Connected Devices** or **DHCP Clients**
3. Look for "Creality", "K1", or the printer's hostname
4. Note the IP address

### Method 3: Network Scanner App
1. Download a network scanner:
   - **Mobile**: "Fing" (iOS/Android)
   - **Desktop**: "Advanced IP Scanner" (Windows) or "Angry IP Scanner" (Mac/Linux)
2. Scan your local network
3. Look for new devices with manufacturer "Creality"

### Method 4: Command Line (Advanced)
```bash
# Scan your network (replace 192.168.1.0 with your network)
nmap -sn 192.168.1.0/24 | grep -B 2 "Creality"

# Or try pinging the common hostname
ping creality-k1.local
```

---

## ⚙️ Advanced Configuration

### Custom Ports

If your printer uses non-standard ports:

1. During setup, change the port values:
   - **HTTP Port**: Default is `9999`
   - **WebSocket Port**: Default is `9999`

2. Verify the ports are open:
   ```bash
   # Test HTTP port
   curl http://YOUR_PRINTER_IP:9999/
   
   # Test WebSocket (using websocat tool)
   websocat ws://YOUR_PRINTER_IP:9999/websocket
   ```

### Multiple Printers

To add multiple printers:

1. Complete setup for first printer
2. Go to **Settings** → **Devices & Services**
3. Click **+ Add Integration** again
4. Select **"Creality Connect"**
5. Enter details for second printer
6. Repeat for additional printers

Each printer will appear as a separate device with its own entities.

---

## 🧪 Verification & Testing

### Check Integration Status

1. Go to **Settings** → **Devices & Services**
2. Find **"Creality Connect"**
3. Verify status is **OK** (not "Failed to setup")

### Check Device & Entities

1. Click on the printer device
2. You should see:
   - ✅ **20+ sensor entities** (temperatures, position, progress, etc.)
   - ✅ **3 binary sensors** (printing, paused, LED)
   - ✅ **2 switches** (LED, pause/resume)
   - ✅ **5 number controls** (fans, temperatures)
   - ✅ **5 buttons** (cancel, home)
   - ✅ **1 camera** (webcam stream)
   - ✅ **1 image** (print preview)

### Test Real-time Updates

1. Start a print on your printer
2. Watch the sensors in Home Assistant
3. You should see:
   - Progress percentage increasing
   - Temperatures rising
   - State changing to "printing"
   - Layer count increasing

### Test Controls

**Test LED Switch:**
1. Go to the LED switch entity
2. Toggle it on/off
3. Verify the printer's LED light responds

**Test Fan Control:**
1. Find a fan number entity
2. Adjust the slider
3. Listen for fan speed change on printer

**Test Temperature:**
1. Set nozzle or bed target temperature
2. Monitor actual temperature sensor
3. Temperature should start rising toward target

---

## 🐛 Troubleshooting

### Problem: Integration not showing in setup

**Solutions:**
1. Verify files are in correct location:
   ```bash
   ls -la /config/custom_components/creality_connect/
   ```
2. Check file permissions:
   ```bash
   chmod -R 755 /config/custom_components/creality_connect/
   ```
3. Check logs for errors:
   - **Settings** → **System** → **Logs**
   - Look for errors mentioning "creality_connect"

### Problem: "Cannot connect" error during setup

**Solutions:**
1. **Verify IP address:**
   ```bash
   ping YOUR_PRINTER_IP
   ```
2. **Check if port 9999 is accessible:**
   ```bash
   curl http://YOUR_PRINTER_IP:9999/
   ```
3. **Check firewall settings** on your network
4. **Restart printer** and try again

### Problem: Entities show "Unavailable"

**Solutions:**
1. **Check WebSocket connection:**
   - View logs: **Settings** → **System** → **Logs**
   - Look for "WebSocket" errors
2. **Reload integration:**
   - **Settings** → **Devices & Services**
   - Click "⋮" on Creality Connect
   - Select **Reload**
3. **Restart Home Assistant**

### Problem: Webcam not working

**Solutions:**
1. **Test stream URL directly:**
   - Open in browser: `http://YOUR_PRINTER_IP:8080/?action=stream`
2. **Verify webcam is enabled** on printer
3. **Check port 8080 is accessible**

### Problem: Controls not working

**Solutions:**
1. **Verify WebSocket is connected** (check logs)
2. **Test with printer's own interface** to rule out hardware issues
3. **Check printer is not in error state**

---

## 📝 Logs & Debugging

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.creality_connect: debug
```

Restart Home Assistant, then:
1. **Settings** → **System** → **Logs**
2. Look for lines starting with `custom_components.creality_connect`

### Common Log Messages

**Good:**
```
✓ Connected to printer at 192.168.1.100:9999
✓ WebSocket connected
✓ Received Creality format data
```

**Bad:**
```
⚠️ Cannot reach printer at 192.168.1.100:9999
⚠️ WebSocket connection failed
⚠️ Failed to decode WebSocket message
```

---

## 🔄 Updating the Integration

### Manual Update

1. Download the latest release
2. Stop Home Assistant
3. Replace files in `custom_components/creality_connect/`
4. Start Home Assistant
5. Clear browser cache (Ctrl+Shift+R)

### HACS Update (when available)

1. Open HACS
2. Go to **Integrations**
3. Find **"Creality Connect"**
4. Click **Update** if available
5. Restart Home Assistant

---

## 🗑️ Uninstalling

### Step 1: Remove Integration from UI

1. Go to **Settings** → **Devices & Services**
2. Find **"Creality Connect"**
3. Click **"⋮"** (three dots)
4. Select **"Delete"**
5. Confirm deletion

### Step 2: Remove Files

```bash
rm -rf /config/custom_components/creality_connect/
```

### Step 3: Restart Home Assistant

All entities and devices will be removed.

---

## 🆘 Getting Help

If you're still having issues:

1. **Check existing issues:** [GitHub Issues](https://github.com/shihanpietersz/creality_connect/issues)
2. **Create a new issue:** Include:
   - Home Assistant version
   - Printer model
   - Error messages from logs
   - Steps to reproduce
3. **Community support:** [Home Assistant Community Forum](https://community.home-assistant.io/)

---

**Installation complete! Enjoy controlling your 3D printer from Home Assistant! 🎉**
