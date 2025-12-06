# 📹 Camera Setup Guide - Getting Robot Camera Feed in VR

## Overview

To see the robot's camera feed in your Quest 3 headset, you need to set up the **teleimager** service on the robot's PC2 (the robot's onboard computer). This service streams the robot's head camera to your Mac, which then displays it in VR.

## Current Status

**Your Setup**: You're running teleoperation from your Mac, but the camera service needs to run on the **robot's PC2** (IP: 192.168.123.164).

## Architecture

```
Robot PC2 (192.168.123.164)
    ↓ (teleimager service)
Camera Stream (ZMQ/WebRTC)
    ↓ (network)
Your Mac (192.168.123.56)
    ↓ (image_client)
VR Headset (Quest 3)
```

## Step-by-Step Setup

### Step 1: Install teleimager on Robot PC2

**SSH into the robot's PC2:**

```bash
# From your Mac, SSH into robot
ssh unitree@192.168.123.164

# On PC2, clone teleimager
cd ~
git clone https://github.com/silencht/teleimager
cd teleimager
```

### Step 2: Install Dependencies on PC2

```bash
# Install system dependencies
sudo apt install -y libusb-1.0-0-dev libturbojpeg-dev

# Create conda environment (if not exists)
conda create -n teleimager python=3.10 -y
conda activate teleimager

# Install teleimager
pip install -e .

# Set up UVC permissions
bash setup_uvc.sh
```

### Step 3: Copy SSL Certificates

**From your Mac**, copy the certificates to PC2:

```bash
# From your Mac terminal
cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop/televuer
scp cert.pem key.pem unitree@192.168.123.164:~/teleimager/
```

**On PC2**, configure certificate location:

```bash
# On PC2
mkdir -p ~/.config/xr_teleoperate/
cp ~/teleimager/cert.pem ~/teleimager/key.pem ~/.config/xr_teleoperate/
```

### Step 4: Find Your Camera

**On PC2**, discover connected cameras:

```bash
# On PC2
conda activate teleimager
cd ~/teleimager
python -m teleimager.image_server --cf
```

This will show you:
- `video_id` (e.g., `/dev/video0`)
- `serial_number` (e.g., `01.00.00`)
- `physical_path` (USB path)
- Supported formats and resolutions

### Step 5: Configure Camera

**On PC2**, edit the config file:

```bash
# On PC2
cd ~/teleimager
nano cam_config_server.yaml
```

**Example configuration** (adjust based on your camera discovery):

```yaml
head_camera:
  # Enable ZMQ (for local Mac connection)
  enable_zmq: true
  zmq_port: 55555
  
  # Enable WebRTC (for browser/VR)
  enable_webrtc: true
  webrtc_port: 60001
  
  # Camera type
  type: uvc  # or "opencv" or "realsense"
  
  # Image settings
  image_shape: [480, 1280]  # [height, width]
  binocular: true  # true if stereo camera
  fps: 60
  
  # Camera identifier (use values from --cf discovery)
  video_id: 0
  serial_number: 01.00.00
  physical_path: null
```

### Step 6: Start Image Server on PC2

```bash
# On PC2
conda activate teleimager
cd ~/teleimager
python -m teleimager.image_server
```

**You should see:**
- Camera initialized
- ZMQ server started on port 55555
- WebRTC server started on port 60001

### Step 7: Test Camera Connection

**Option A: Test with image_client (on your Mac)**

```bash
# On your Mac
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate xr_teleop
cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop/teleimager/src
python -m teleimager.image_client --host 192.168.123.164
```

**Option B: Test with WebRTC (in browser)**

1. Open browser on your Mac
2. Go to: `https://192.168.123.164:60001`
3. Click "Advanced" → "Proceed to IP (unsafe)"
4. Click "Start" button
5. You should see camera feed

### Step 8: Verify Teleoperation Script Configuration

**Your teleoperation script** (`teleop_hand_and_arm.py`) should already be configured correctly:

```python
# The script uses:
img_client = ImageClient(host=args.img_server_ip)  # 192.168.123.164
```

**Make sure you're running with:**
```bash
--img-server-ip=192.168.123.164
```

## Display Modes

The camera feed appears differently based on `--display-mode`:

### `--display-mode=immersive` (Current)
- **Full VR view** - Robot's camera feed fills entire VR view
- **Requires**: ZMQ or WebRTC enabled
- **Best for**: Full immersion

### `--display-mode=pass-through`
- **No camera feed** - Shows real world through Quest cameras
- **Camera still streams** - But not displayed in VR
- **Best for**: Seeing real world while controlling robot

### `--display-mode=ego`
- **Small window** - Robot camera in center, real world around it
- **Requires**: ZMQ or WebRTC enabled
- **Best for**: Mixed reality experience

## Troubleshooting

### "Request to 192.168.123.164:60000 timed out"
- **This is normal!** - Port 60000 is camera config server
- **Script uses local config** - Falls back to `cam_config_server.yaml`
- **Not a problem** - Teleoperation still works

### "No camera feed in VR"
- **Check teleimager is running** - On PC2
- **Check network** - Can you ping 192.168.123.164?
- **Check ports** - Firewall blocking 55555 or 60001?
- **Check display mode** - Must be `immersive` or `ego` (not `pass-through`)

### "Camera not found"
- **Run camera discovery** - `python -m teleimager.image_server --cf`
- **Check camera ID** - Update `cam_config_server.yaml`
- **Check permissions** - Run `bash setup_uvc.sh` on PC2

### "WebRTC certificate error"
- **Copy certificates** - From Mac to PC2
- **Check certificate path** - `~/.config/xr_teleoperate/`
- **Trust certificate** - In browser, click "Advanced" → "Proceed"

### "Black screen in VR"
- **Wait for 'r'** - Camera feed starts after pressing 'r'
- **Check teleimager** - Is it running on PC2?
- **Check ZMQ/WebRTC** - Are they enabled in config?

## Quick Start Checklist

- [ ] SSH into robot PC2 (192.168.123.164)
- [ ] Install teleimager on PC2
- [ ] Copy SSL certificates to PC2
- [ ] Discover cameras (`--cf`)
- [ ] Configure `cam_config_server.yaml`
- [ ] Start `teleimager.image_server` on PC2
- [ ] Test connection (image_client or browser)
- [ ] Run teleoperation with `--img-server-ip=192.168.123.164`
- [ ] Press 'r' to start (camera feed should appear)

## Alternative: Local Camera (For Testing)

If you want to test with a local camera on your Mac (not robot's camera):

1. **Connect USB camera to Mac**
2. **Run teleimager locally**:
   ```bash
   # On Mac
   conda activate xr_teleop
   cd dependencies/xr_teleoperate/teleop/teleimager
   python -m teleimager.image_server --cf  # Find camera
   # Edit cam_config_server.yaml with your camera
   python -m teleimager.image_server
   ```
3. **Run teleoperation with**:
   ```bash
   --img-server-ip=127.0.0.1  # or your Mac's IP
   ```

## Summary

- 📹 **Camera service runs on robot PC2** (not your Mac)
- 🔐 **Need SSL certificates** for WebRTC
- ⚙️ **Configure camera** in `cam_config_server.yaml`
- 🚀 **Start teleimager** on PC2 before teleoperation
- ✅ **Test connection** before using in VR
- 🎮 **Camera feed appears** after pressing 'r' in teleoperation

