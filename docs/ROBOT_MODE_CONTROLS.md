# Robot Mode Controls

## Remote Control (Manual)

### Debug Mode
- **L2 + R2** (hold both) → then **L2 + A**
- Used for: Arm teleoperation without locomotion

### Motion Mode (Regular)
- **R1 + X**
- Used for: Locomotion controls, normal operation

### Motion Mode (Running)
- **R2 + A**
- Used for: Running/locomotion mode

### Damp Mode
- **L1 + R1** (hold both)
- Used for: Soft stop, low power state

## Terminal Control (Programmatic)

Use the `switch_robot_mode.py` script to switch modes from terminal:

### Enter Debug Mode
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py debug en7
```

### Enter Motion Mode (AI Mode)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py motion en7
```

### Enter Damp Mode
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py damp en7
```

### Check Current Mode
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py check en7
```

## Mode Usage Guide

| Mode | When to Use | Teleoperation Support |
|------|-------------|----------------------|
| **Debug Mode** | Arm teleoperation only (no locomotion) | ✅ Arms only |
| **Motion Mode** | Locomotion + arm control | ✅ Arms + Legs |
| **Damp Mode** | Safe stop, low power | ❌ No control |

## Quick Reference

**For controller mode + locomotion:**
1. Put robot in **Motion Mode** (terminal or remote)
2. Run teleoperation with `--input-mode=controller --enable-locomotion`

**For arm-only teleoperation:**
1. Put robot in **Debug Mode** (terminal or remote)
2. Run teleoperation with `--input-mode=controller` (no `--enable-locomotion`)

