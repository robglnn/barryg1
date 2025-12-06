# Robot Mode Controls

## Remote Control (Manual Button Combinations)

### Development Mode
- **L2 + R2** (hold both triggers simultaneously)
- **Purpose**: First step to enter Debug Mode
- **What it does**: Releases any current high-level mode, enters Development Mode
- **Note**: This is a prerequisite for Debug Mode

### Debug Mode
- **Step 1**: **L2 + R2** (hold both) → Enters Development Mode
- **Step 2**: **L2 + A** → Enters Debug Mode
- **Purpose**: Arm teleoperation without locomotion
- **Supports**: 
  - ✅ Arm control via controllers/hand tracking
  - ✅ Video streaming
  - ❌ Leg locomotion (not supported in Debug Mode)

### Motion Mode (Regular Mode)
- **R1 + X** (press both simultaneously)
- **Purpose**: Full robot control with locomotion
- **Supports**:
  - ✅ Arm control via controllers/hand tracking
  - ✅ Leg locomotion (walking, turning, strafing)
  - ✅ Video streaming
  - ✅ All features simultaneously

### Motion Mode (Running Mode)
- **R2 + A** (press both simultaneously)
- **Purpose**: Running/locomotion mode (faster movement)
- **Supports**: Same as Regular Motion Mode but optimized for running

### Locked Standing Mode
- **L2 + Up Arrow** (hold L2, press Up on D-pad)
- **Purpose**: Stable locked standing position
- **When to use**: After entering Motion Mode, before starting locomotion
- **What it does**: Robot enters balanced standing state, ready for movement commands

### Damp Mode
- **L1 + R1** (hold both simultaneously)
- **Purpose**: Soft stop, low power state
- **What it does**: Robot motors are damped, safe stop state
- **Use case**: Emergency stop or when robot needs to be stationary

## Terminal Control (Programmatic)

Use the `switch_robot_mode.py` script to switch modes from terminal:

### Enter Development Mode
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py dev en7
```

### Enter Debug Mode (requires Dev Mode first)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py debug en7
```

### Enter Motion Mode (Regular Mode - R1+X)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py motion en7
```

### Enter Locked Standing Mode (L2+Up)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python3 switch_robot_mode.py stand en7
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

| Mode | Remote Command | When to Use | Teleoperation Support |
|------|---------------|-------------|----------------------|
| **Development Mode** | L2+R2 | First step to Debug Mode | ❌ No control |
| **Debug Mode** | L2+R2, then L2+A | Arm teleoperation only (no locomotion) | ✅ Arms only |
| **Motion Mode (Regular)** | R1+X | Locomotion + arm control | ✅ Arms + Legs |
| **Motion Mode (Running)** | R2+A | Running/locomotion mode | ✅ Arms + Legs |
| **Locked Standing** | L2+Up | Stable standing in Motion Mode | ✅ Prepares for locomotion |
| **Damp Mode** | L1+R1 | Safe stop, low power | ❌ No control |

## Quick Reference

**For controller mode + locomotion:**
1. Put robot in **Motion Mode** (R1+X on remote, or CLI option 3)
2. Enter **Locked Standing** (L2+Up on remote, or CLI option 4)
3. Run teleoperation with `--input-mode=controller --enable-locomotion`

**For arm-only teleoperation:**
1. Put robot in **Development Mode** (L2+R2 on remote, or CLI option 1)
2. Enter **Debug Mode** (L2+A on remote, or CLI option 2)
3. Run teleoperation with `--input-mode=controller` (no `--enable-locomotion`)

## Controller Button Reference

### Triggers
- **L1**: Left trigger 1
- **L2**: Left trigger 2 (hold for combinations)
- **R1**: Right trigger 1
- **R2**: Right trigger 2 (hold for combinations)

### Face Buttons
- **A**: Action button
- **B**: Back button
- **X**: X button
- **Y**: Y button

### D-Pad
- **Up**: Up arrow
- **Down**: Down arrow
- **Left**: Left arrow
- **Right**: Right arrow

### Common Combinations
- **L2+R2**: Development Mode
- **L2+A**: Debug Mode (after Dev Mode)
- **R1+X**: Motion Mode (Regular)
- **R2+A**: Motion Mode (Running)
- **L2+Up**: Locked Standing
- **L1+R1**: Damp Mode
