# 🎮 Locomotion Controls Added!

## What Was Added

Added **locomotion controls** using Quest controller joysticks, even when using **hand tracking mode** for arm control!

## How It Works

### Control Mapping

- **Left Joystick**:
  - **Y-axis (forward/back)**: Forward/backward movement
  - **X-axis (left/right)**: Strafe left/right
- **Right Joystick**:
  - **X-axis**: Spin/turn left/right

### Velocity Limits

- **Max speed**: 0.3 m/s (for safety)
- **Dead zone**: < 0.01 (joysticks must move at least 1% to register)
- **Auto-stop**: Robot stops when joysticks are centered

## How to Use

### Enable Locomotion

Add `--enable-locomotion` flag to your command:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --enable-locomotion
```

### Robot Mode Requirements

⚠️ **IMPORTANT**: Locomotion requires the robot to be in **Motion Mode**, not Debug Mode!

**To enable Motion Mode:**
1. **On robot remote**: Press **R1 + X** simultaneously
2. **Or use robot app**: Select "Motion Mode" or "Regular Mode"
3. **Robot should beep/indicate** motion mode is active

**Note**: In Motion Mode, arm control via hand tracking should still work, but test carefully!

### Using Locomotion

1. **Hold Quest controllers** (even though you're using hand tracking for arms)
2. **Left joystick**:
   - Push **forward** → Robot moves forward
   - Pull **back** → Robot moves backward
   - Push **left** → Robot strafes left
   - Push **right** → Robot strafes right
3. **Right joystick**:
   - Push **left** → Robot spins/turns left
   - Push **right** → Robot spins/turns right

### Emergency Stop

**Both thumbsticks pressed simultaneously** → Robot enters Damp Mode (soft emergency stop)

## Technical Details

### Implementation

- **LocoClientWrapper**: Uses G1 locomotion client via DDS
- **Velocity command**: `Move(vx, vy, vyaw)` where:
  - `vx`: Forward/backward velocity (m/s)
  - `vy`: Left/right velocity (m/s)
  - `vyaw`: Rotational velocity (rad/s)
- **Continuous updates**: Commands sent every control loop (~30 Hz)

### Code Location

- **Initialization**: `teleop_hand_and_arm.py` line ~199-215
- **Control loop**: `teleop_hand_and_arm.py` line ~408-430
- **Locomotion client**: `utils/motion_switcher.py` → `LocoClientWrapper`

## Safety Features

1. **Velocity limit**: Max 0.3 m/s (configurable in code)
2. **Dead zone**: Prevents drift from joystick noise
3. **Auto-stop**: Robot stops when joysticks released
4. **Emergency stop**: Both thumbsticks = Damp Mode
5. **Exit button**: Right A button = quit teleoperation

## Troubleshooting

### "Failed to initialize LocoClientWrapper"
- **Cause**: Robot not in Motion Mode
- **Solution**: Put robot in Motion Mode (R1+X)

### "Robot doesn't move"
- **Check**: Robot is in Motion Mode
- **Check**: Controllers are being tracked (check Quest)
- **Check**: Joysticks are being pushed (not just touched)
- **Check**: Dead zone - need to push joystick at least 1%

### "Robot moves but arms don't work"
- **Cause**: Motion Mode may interfere with arm control
- **Solution**: Test carefully - may need to adjust mode or code

### "Robot moves too fast/slow"
- **Adjust**: Change velocity multiplier in code (currently `* 0.3`)
- **Location**: Line ~418-420 in `teleop_hand_and_arm.py`

## Current Limitations

1. **Mode conflict**: Locomotion needs Motion Mode, arms work in Debug Mode
   - **Workaround**: Test if arms still work in Motion Mode
   - **Future**: May need hybrid mode support

2. **No simultaneous mode**: Can't be in Debug Mode (for arms) and Motion Mode (for locomotion) simultaneously
   - **Current**: Must choose one mode
   - **Test**: See if Motion Mode allows both

## Testing Recommendations

1. **Start with slow movements**: Test forward/back first
2. **Test turning**: Use right joystick carefully
3. **Test arm control**: Verify hand tracking still works in Motion Mode
4. **Emergency stop**: Test both thumbsticks = Damp Mode
5. **Gradual increase**: Start with small joystick movements

## Summary

✅ **Locomotion controls added!**  
✅ **Works with hand tracking mode!**  
✅ **Left joystick: forward/back/left/right**  
✅ **Right joystick: spin/turn**  
⚠️ **Requires Motion Mode** (not Debug Mode)  
⚠️ **Test carefully** - may affect arm control

Try it out and let me know how it works!

