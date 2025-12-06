# Unitree XR Teleoperation Setup for Meta Quest 3

## Repository Cloned ✅

The Unitree XR teleoperation repository has been successfully cloned:
- **Location**: `dependencies/xr_teleoperate/`
- **Repository**: https://github.com/unitreerobotics/xr_teleoperate
- **Purpose**: Control Unitree G1 EDU (23 DOF) robot using Meta Quest 3 VR headset

## Overview

This system enables **teleoperation** of Unitree humanoid robots using XR devices:
- **Supported XR Devices**: Apple Vision Pro, PICO 4 Ultra Enterprise, **Meta Quest 3**
- **Supported Robots**: G1 (23 DoF and 29 DoF), H1 (4-DoF and 7-DoF arms)
- **Features**:
  - Real-time robot control via VR headset
  - Hand tracking and controller support
  - First-person view from robot's cameras
  - Data recording for imitation learning
  - Inverse kinematics for precise arm control

## System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Meta Quest │◄───────►│  Host PC     │◄───────►│  Robot PC2  │
│      3      │  WebRTC │  (This Mac)  │  DDS    │  (G1 Robot) │
└─────────────┘         └──────────────┘         └─────────────┘
```

## Installation Steps

### 1. Initialize Submodules

```bash
cd dependencies/xr_teleoperate
git submodule update --init --depth 1
```

### 2. Install Python Dependencies

The repository requires Python 3.10 and several packages. On macOS, you can use conda or venv:

**Option A: Using Conda (Recommended)**
```bash
conda create -n xr_teleop python=3.10 -c conda-forge
conda activate xr_teleop
conda install pinocchio=3.1.0 numpy=1.26.4 -c conda-forge
pip install -r dependencies/xr_teleoperate/requirements.txt
```

**Option B: Using venv**
```bash
python3.10 -m venv venv_xr_teleop
source venv_xr_teleop/bin/activate
pip install -r dependencies/xr_teleoperate/requirements.txt
```

### 3. Install Submodules

```bash
# Install teleimager (image service)
cd dependencies/xr_teleoperate/teleop/teleimager
pip install -e . --no-deps

# Install televuer (XR device interface)
cd ../televuer
pip install -e .
```

### 4. Install Unitree SDK2 Python

```bash
cd dependencies
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python
pip install -e .
```

### 5. Configure SSL Certificates

For secure WebRTC connection with Meta Quest 3:

```bash
cd dependencies/xr_teleoperate/teleop/televuer

# Generate certificate files for Quest 3
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem

# Configure certificate paths
mkdir -p ~/.config/xr_teleoperate/
cp cert.pem key.pem ~/.config/xr_teleoperate/

# Or set environment variables
export XR_TELEOP_CERT="$HOME/Documents/barryg1/dependencies/xr_teleoperate/teleop/televuer/cert.pem"
export XR_TELEOP_KEY="$HOME/Documents/barryg1/dependencies/xr_teleoperate/teleop/televuer/key.pem"
```

### 6. Network Configuration

Ensure your Mac and Meta Quest 3 are on the same network:

1. Find your Mac's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Note the IP address (e.g., `192.168.1.100`)

3. Configure firewall (if needed):
   ```bash
   # Allow port 8012 for WebRTC
   # macOS uses pfctl, but you may need to configure through System Settings
   ```

## Usage

### For Simulation (Testing)

```bash
conda activate xr_teleop  # or: source venv_xr_teleop/bin/activate
cd dependencies/xr_teleoperate/teleop

# Launch with G1 23 DOF configuration
python teleop_hand_and_arm.py \
    --xr-mode=hand \
    --arm=G1_23 \
    --input-mode=hand \
    --display-mode=immersive \
    --sim
```

### For Physical Robot

1. **Start Image Service on Robot PC2** (if not already running):
   - The robot's PC2 should run the `teleimager` service
   - This streams camera feeds to your Mac

2. **Launch Teleoperation on Host (Mac)**:
   ```bash
   conda activate xr_teleop
   cd dependencies/xr_teleoperate/teleop
   
   python teleop_hand_and_arm.py \
       --xr-mode=hand \
       --arm=G1_23 \
       --input-mode=hand \
       --display-mode=immersive \
       --img-server-ip=192.168.123.164  # Robot PC2 IP
   ```

3. **Connect Meta Quest 3**:
   - Put on your Quest 3 headset
   - Connect to the same Wi-Fi network
   - Open browser (Quest Browser) and navigate to:
     ```
     https://YOUR_MAC_IP:8012/?ws=wss://YOUR_MAC_IP:8012
     ```
   - Accept the security warning (self-signed certificate)
   - Click "Virtual Reality" button
   - Allow VR permissions

4. **Start Teleoperation**:
   - Align your arms to robot's initial pose
   - Press **r** in the terminal to begin
   - Control the robot with your hands!

## Key Parameters

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| `--arm` | Robot arm type | `G1_29`, `G1_23`, `H1_2`, `H1` | `G1_29` |
| `--ee` | End-effector type | `dex1`, `dex3`, `inspire_ftp`, `inspire_dfx`, `brainco` | None |
| `--input-mode` | Control method | `hand` (hand tracking), `controller` | `hand` |
| `--display-mode` | View mode | `immersive`, `ego`, `pass-through` | `immersive` |
| `--frequency` | Control FPS | Any float | 30.0 |
| `--img-server-ip` | Robot camera server IP | IPv4 address | `192.168.123.164` |
| `--motion` | Enable motion control | Flag | Disabled |
| `--record` | Enable data recording | Flag | Disabled |

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
- Ensure certificates are in `~/.config/xr_teleoperate/` or environment variables are set

### Connection Issues
- Verify Mac and Quest 3 are on the same network
- Check firewall settings for port 8012
- Verify robot PC2 IP address is correct

### Hand Tracking Not Working
- Ensure Quest 3 hand tracking is enabled in settings
- Try `--input-mode=controller` as alternative
- Check Quest 3 firmware is up to date

## Additional Resources

- [Official Unitree Documentation](https://support.unitree.com/home/zh/Teleoperation)
- [Repository Wiki](https://github.com/unitreerobotics/xr_teleoperate/wiki)
- [Video Demo](https://www.youtube.com/watch?v=pNjr2f_XHoo)

## Next Steps

1. Initialize submodules: `git submodule update --init --depth 1`
2. Set up Python environment with dependencies
3. Install unitree_sdk2_python
4. Configure SSL certificates
5. Test with simulation first
6. Connect to physical robot

