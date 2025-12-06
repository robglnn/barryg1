# Unitree G1 EDU Development Environment

This project provides a complete development environment for controlling the Unitree G1 EDU robot (23 DOF) using:
- **Unitree SDK2** - Robot control SDK
- **MuJoCo** - Physics simulation
- **Cyclone DDS** - Communication middleware
- **XR Teleoperation** - VR control with Meta Quest 3

## 🎉 Current Status: Stable Arm Control with Visual Passthrough

✅ **Fully operational** - Quest controllers provide real-time arm control with first-person video streaming in VR. Full arm movement (shoulders, elbows, wrists) working correctly with DDS video passthrough to Quest VR headset.

## 🚧 Planned Features

- **Audio Passthrough**: Bidirectional audio between Quest 3 and robot (microphone ↔ speakers)
- **Hip Lean Control**: Control robot body pitch using Quest right joystick forward/back
- See `docs/PRD_AUDIO_AND_HIP_CONTROL.md` for detailed requirements

## Project Structure

```
barryg1/
├── dependencies/
│   ├── cyclonedds/          # Cyclone DDS (built and installed)
│   ├── mujoco/              # MuJoCo (installed via pip)
│   ├── unitree_sdk2/        # Unitree SDK2 (cloned, macOS fixes applied)
│   └── xr_teleoperate/     # XR teleoperation for Quest 3
├── docs/                    # All documentation files
├── memory-bank/             # Project memory and context
├── install.sh               # Installation script
├── build.sh                 # Build script
├── robot_control_cli.py     # Interactive CLI menu
├── switch_robot_mode.py     # Robot mode switcher script
├── START_CLI.txt            # Quick start command for CLI
└── README.md                # This file
```

## Quick Start

### 1. Prerequisites

- macOS (tested on macOS 13+)
- Homebrew
- Python 3.8+ (3.10 recommended for XR teleoperation)
- Xcode Command Line Tools

### 2. Install System Dependencies

```bash
brew install cmake pkg-config eigen boost yaml-cpp spdlog fmt
```

### 3. Environment Setup

Add to your `~/.zshrc`:

```bash
# Unitree G1 Development Environment
export CYCLONEDDS_HOME="$HOME/Documents/barryg1/dependencies/cyclonedds/install"
export MUJOCO_HOME="$(python3 -c 'import mujoco; import os; print(os.path.dirname(mujoco.__file__))')"
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc
```

### 4. Start Robot Control CLI

The easiest way to control the robot is through the interactive CLI menu:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 robot_control_cli.py
```

Or use the quick start file:
```bash
cat START_CLI.txt | bash
```

**CLI Features:**
- Switch robot modes (Debug, Motion, Damp) with single key presses
- Launch teleoperation with different configurations
- Control teleoperation (start with 'r', safe exit with 'q')
- Check robot and teleoperation status
- All from one interactive menu

See `docs/ROBOT_MODE_CONTROLS.md` for detailed mode information.

## Components

### ✅ Unitree SDK2
- **Status**: Cloned and configured
- **Location**: `dependencies/unitree_sdk2/`
- **macOS Compatibility**: Fixed (see BUILD_STATUS.md)

### ✅ MuJoCo
- **Status**: Installed (Python package)
- **Version**: 3.3.7
- **Usage**: `import mujoco`

### ✅ Cyclone DDS
- **Status**: Built and installed
- **Location**: `dependencies/cyclonedds/install/`

### ✅ XR Teleoperation
- **Status**: Repository cloned
- **Location**: `dependencies/xr_teleoperate/`
- **Purpose**: Control robot with Meta Quest 3
- **Setup**: See `XR_TELEOPERATION_SETUP.md`

## Next Steps

1. **Start the CLI**: Run the command above to launch the interactive control menu
2. **For Robot Control**: Use Unitree SDK2 examples in `dependencies/unitree_sdk2/example/`
3. **For VR Control**: Follow `docs/XR_TELEOPERATION_SETUP.md` to set up Meta Quest 3 teleoperation
4. **For Simulation**: Set up MuJoCo simulation environment (see `docs/ISAAC_SIM_MACOS_LIMITATION.md` for macOS limitations)

## Documentation

All documentation is in the `docs/` directory:

- **Setup & Installation:**
  - `INSTALLATION_GUIDE.md` - Complete installation instructions
  - `BUILD_STATUS.md` - Current build status and known issues
  - `XR_TELEOPERATION_SETUP.md` - VR teleoperation setup guide
  - `SETUP_STATUS.md` - Installation status summary

- **Robot Control:**
  - `ROBOT_MODE_CONTROLS.md` - Robot mode switching guide
  - `PHYSICAL_ROBOT_CONTROL.md` - Physical robot control setup
  - `ROBOT_MODE_GUIDE.md` - Detailed mode information

- **XR Teleoperation:**
  - `HAND_TRACKING_VS_CONTROLLER_MODE.md` - Input mode differences
  - `QUEST_3_USAGE_GUIDE.md` - Quest 3 usage instructions
  - `LOCOMOTION_CONTROLS_ADDED.md` - Locomotion control guide
  - `CAMERA_SETUP_GUIDE.md` - Camera/video setup

- **Troubleshooting:**
  - `TROUBLESHOOTING.md` - General troubleshooting
  - `DDS_TROUBLESHOOTING.md` - DDS connection issues
  - `QUEST_BROWSER_TROUBLESHOOTING.md` - Quest browser issues
  - `FIREWALL_TROUBLESHOOTING.md` - Network/firewall issues

- **Technical Details:**
  - `DDS_VIDEO_INTEGRATION_COMPLETE.md` - DDS video streaming
  - `HYBRID_DDS_APPROACH.md` - DDS connection approach
  - Various fix and implementation notes

## Resources

- [Unitree SDK2 GitHub](https://github.com/unitreerobotics/unitree_sdk2)
- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [Cyclone DDS Documentation](https://cyclonedds.io/)
- [XR Teleoperation Repository](https://github.com/unitreerobotics/xr_teleoperate)
- [Unitree G1 Documentation](https://www.unitree.com/products/g1)

## License

Please refer to individual component licenses:
- Unitree SDK2: Check repository license
- MuJoCo: Apache 2.0
- Cyclone DDS: Eclipse Public License 2.0
- XR Teleoperation: Check repository license
