# XR Teleoperation Setup Complete ✅

## Installation Summary

The XR teleoperation system for controlling your Unitree G1 EDU (23 DOF) with Meta Quest 3 has been successfully set up!

### ✅ Completed Components

1. **Python Environment** (Python 3.10.19)
   - Virtual environment: `venv_xr_teleop_py310/`
   - Location: `/Users/hg/Documents/barryg1/venv_xr_teleop_py310/`

2. **Core Dependencies**
   - ✅ matplotlib, rerun-sdk, meshcat, sshkeyboard
   - ✅ pinocchio (inverse kinematics)
   - ✅ casadi (optimization)

3. **XR Teleoperation Submodules**
   - ✅ teleimager (image streaming service)
   - ✅ televuer (XR device interface)
   - ✅ dex-retargeting (hand retargeting)

4. **Unitree SDK2 Python**
   - ✅ unitree_sdk2py (robot communication)
   - ✅ cyclonedds (DDS middleware)

5. **SSL Certificates**
   - ✅ Generated for WebRTC connection
   - ✅ Location: `dependencies/xr_teleoperate/teleop/televuer/`
   - ✅ Copied to: `~/.config/xr_teleoperate/`

## Quick Start

### 1. Activate Environment

```bash
cd /Users/hg/Documents/barryg1
source venv_xr_teleop_py310/bin/activate
```

### 2. Find Your Mac's IP Address

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Note your IP address (e.g., `192.168.1.100`)

### 3. Launch Teleoperation

For **simulation** (testing):
```bash
cd dependencies/xr_teleoperate/teleop
python teleop_hand_and_arm.py \
    --xr-mode=hand \
    --arm=G1_23 \
    --input-mode=hand \
    --display-mode=immersive \
    --sim
```

For **physical robot**:
```bash
cd dependencies/xr_teleoperate/teleop
python teleop_hand_and_arm.py \
    --xr-mode=hand \
    --arm=G1_23 \
    --input-mode=hand \
    --display-mode=immersive \
    --img-server-ip=192.168.123.164  # Robot PC2 IP
```

### 4. Connect Meta Quest 3

1. Put on your Quest 3 headset
2. Connect to the same Wi-Fi network as your Mac
3. Open Quest Browser
4. Navigate to: `https://YOUR_MAC_IP:8012/?ws=wss://YOUR_MAC_IP:8012`
   - Replace `YOUR_MAC_IP` with your actual IP address
5. Accept the security warning (self-signed certificate)
6. Click "Virtual Reality" button
7. Allow VR permissions

### 5. Start Teleoperation

- Align your arms to robot's initial pose
- Press **r** in the terminal to begin
- Control the robot with your hands!

## Environment Variables (Optional)

You can set these in your `~/.zshrc` for convenience:

```bash
# XR Teleoperation
export XR_TELEOP_CERT="$HOME/Documents/barryg1/dependencies/xr_teleoperate/teleop/televuer/cert.pem"
export XR_TELEOP_KEY="$HOME/Documents/barryg1/dependencies/xr_teleoperate/teleop/televuer/key.pem"
```

## Key Parameters

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| `--arm` | Robot arm type | `G1_29`, `G1_23`, `H1_2`, `H1` | `G1_29` |
| `--ee` | End-effector type | `dex1`, `dex3`, `inspire_ftp`, `inspire_dfx`, `brainco` | None |
| `--input-mode` | Control method | `hand`, `controller` | `hand` |
| `--display-mode` | View mode | `immersive`, `ego`, `pass-through` | `immersive` |
| `--frequency` | Control FPS | Any float | 30.0 |
| `--img-server-ip` | Robot camera server IP | IPv4 address | `192.168.123.164` |
| `--motion` | Enable motion control | Flag | Disabled |
| `--record` | Enable data recording | Flag | Disabled |
| `--sim` | Simulation mode | Flag | Disabled |

## Safety Warnings ⚠️

1. **Always maintain a safe distance from the robot**
2. **Read the [Official Documentation](https://support.unitree.com/home/zh/Teleoperation) before use**
3. **In motion mode**:
   - Right controller **A** = Exit teleop
   - Both joysticks pressed = Emergency stop
   - Left joystick = Drive, Right joystick = Turn
4. **Before exiting**: Position robot arms close to initial pose

## Troubleshooting

### Certificate Issues
- If Quest 3 shows security warnings, accept the self-signed certificate
- Certificates are in `~/.config/xr_teleoperate/` or set via environment variables

### Connection Issues
- Verify Mac and Quest 3 are on the same network
- Check firewall settings for port 8012
- Verify robot PC2 IP address is correct

### Hand Tracking Not Working
- Ensure Quest 3 hand tracking is enabled in settings
- Try `--input-mode=controller` as alternative
- Check Quest 3 firmware is up to date

### Missing Dependencies
Some optional dependencies for teleimager may be missing:
- `aiortc` (for WebRTC)
- `pupil-labs-uvc` (for specific cameras)

These are only needed for advanced features.

## Project Structure

```
barryg1/
├── venv_xr_teleop_py310/          # Python 3.10 virtual environment
├── dependencies/
│   ├── xr_teleoperate/            # XR teleoperation repository
│   │   └── teleop/
│   │       ├── teleimager/        # Image streaming
│   │       ├── televuer/          # XR device interface
│   │       └── robot_control/     # Robot control logic
│   └── unitree_sdk2_python/       # Python SDK
└── XR_SETUP_COMPLETE.md           # This file
```

## Next Steps

1. **Test with simulation first** (if available)
2. **Connect to physical robot** when ready
3. **Configure robot PC2** to run teleimager service
4. **Start teleoperating** your G1 EDU!

## Resources

- [XR Teleoperation Repository](https://github.com/unitreerobotics/xr_teleoperate)
- [Official Unitree Documentation](https://support.unitree.com/home/zh/Teleoperation)
- [Repository Wiki](https://github.com/unitreerobotics/xr_teleoperate/wiki)
- [Video Demo](https://www.youtube.com/watch?v=pNjr2f_XHoo)

---

**Setup completed on**: $(date)
**Python version**: 3.10.19
**Environment**: venv_xr_teleop_py310

