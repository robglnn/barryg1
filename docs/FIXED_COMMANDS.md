# Fixed XR Teleoperation Commands

## Issue Fixed ✅

The original error was due to `pinocchio` from pip not having `casadi` support. This has been fixed by:
1. Installing miniconda
2. Creating a conda environment with `pinocchio=3.1.0` (which includes casadi support)
3. Installing all dependencies in the conda environment

## Single-Line Commands (Copy-Paste Ready)

### 1. Launch Teleoperation (Main Command)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive
```

### 2. For Simulation Mode
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --sim
```

### 3. For Physical Robot (with robot IP)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --img-server-ip=192.168.123.164
```

### 4. Find Your Mac's IP
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

### 5. Quest 3 Browser URL
After getting your IP from step 4, open in Quest Browser:
```
https://YOUR_IP:8012/?ws=wss://YOUR_IP:8012
```

### 6. Alternative: Use Startup Script
```bash
/Users/hg/Documents/barryg1/START_XR_TELEOP_FIXED.sh
```

## What Was Fixed

- ✅ Installed miniconda
- ✅ Created conda environment `xr_teleop` with Python 3.10
- ✅ Installed pinocchio 3.1.0 with casadi support via conda
- ✅ Installed all XR teleoperation dependencies
- ✅ Installed teleimager and televuer submodules
- ✅ Installed unitree_sdk2_python
- ✅ Verified pinocchio casadi import works

## Environment Details

- **Conda Environment**: `xr_teleop`
- **Python Version**: 3.10.19
- **Pinocchio Version**: 3.1.0 (with casadi support)
- **Location**: `/opt/homebrew/Caskroom/miniconda/base/envs/xr_teleop`

## Next Steps

1. Run command #1 above to start teleoperation
2. Get your Mac's IP with command #4
3. Open Quest 3 browser with URL from #5
4. Accept security warning
5. Click "Virtual Reality"
6. Press **r** in terminal to begin control

