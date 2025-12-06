# 🤖 Robot Mode Guide for XR Teleoperation

## Current Situation

You're running **without** the `--motion` flag, which means the script needs the robot to be in **Debug Mode**.

## The Problem

The script is trying to automatically enter Debug Mode but failing:
- `Enter debug mode: Failed`
- This means the robot isn't responding to the debug mode command

## Recommended Robot Setup Sequence

Based on Unitree documentation and your available modes:

### Option 1: Try Zero Torque Mode First (Recommended)

1. **Put robot in Zero Torque Mode** (if that's what you have)
2. **Then run the teleoperation script** - it should automatically enter Debug Mode
3. The script's `MotionSwitcher` will try to enter Debug Mode automatically

### Option 2: Use Damp Mode

1. **Put robot in Damp Mode** (L1 + A on remote, or your method)
2. **Wait for robot to stabilize**
3. **Run the teleoperation script**
4. The script should then enter Debug Mode

### Option 3: Use Standing/Ready Mode

1. **Put robot in Standing/Ready Mode** (L1 + UP on remote, or your method)
2. **Run the teleoperation script**
3. The script will try to enter Debug Mode from there

## What the Script Does

When you run **without `--motion` flag**:
1. Script tries to use `MotionSwitcher.Enter_Debug_Mode()`
2. This checks if robot is in a mode, releases it if needed
3. Then enters Debug Mode for teleoperation

## Why It's Failing

The "Enter debug mode: Failed" suggests:
- Robot might be in a mode that can't be released
- Robot's DDS service might not be fully active
- Robot might need to be in a specific initial state

## My Recommendation

**Try this sequence:**

1. **Start with Damp Mode** (safest, zero torque)
   - This gives the script a clean state to work from
   
2. **Run the teleoperation script**
   - It will try to automatically enter Debug Mode
   
3. **If it still fails**, try:
   - **Zero Torque Mode** (if different from Damp)
   - Or **Standing/Ready Mode**

4. **Check the terminal** - you should see:
   - `Enter debug mode: Success` (instead of Failed)
   - `[G1_23_ArmController] Subscribe dds ok.` (instead of waiting)

## Alternative: Use Motion Mode

If Debug Mode keeps failing, you could try using `--motion` flag:

```bash
python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --img-server-ip=192.168.123.164 --motion
```

For motion mode:
- Robot should be in **Control Mode** (via R3 remote: R1 + X)
- This bypasses the Debug Mode requirement

## Next Steps

1. **Try Damp Mode first** - it's the safest starting point
2. **Run the script** and see if Debug Mode succeeds
3. **If it works**, you should see "Subscribe dds ok" and can proceed
4. **If it still fails**, we may need to check robot's DDS service or try motion mode

