# 🛡️ Safe Exit and Neutral Position Guide

## What Happens on Ctrl+C

When you press **Ctrl+C** in the terminal:

1. ✅ **Script catches KeyboardInterrupt**
2. ✅ **Calls `ctrl_dual_arm_go_home()`** - Moves arms to home position (zero angles)
3. ✅ **Takes ~5 seconds** - Arms gradually return to neutral
4. ✅ **Exits Debug Mode** - Robot returns to safe state
5. ✅ **Closes all connections** - DDS, Vuer, image client

**The script handles cleanup automatically!** But you should position arms close to neutral first if possible.

## 🎯 Safest Way to Put Arms in Neutral

### Option 1: Use 'q' Key (Recommended)

**In the terminal** (while script is running):
1. Press **'q'** (not Ctrl+C)
2. Script will:
   - Return arms to home position (~5 seconds)
   - Exit debug mode
   - Clean up gracefully

**This is safer than Ctrl+C** because it's the intended exit method.

### Option 2: Manual Return Before Exit

**Before pressing 'q' or Ctrl+C:**
1. **Move your hands slowly** to match robot's neutral pose:
   - Arms down at sides
   - Elbows slightly bent
   - Hands in front of body
2. **Wait for robot to follow** (may take a moment due to latency)
3. **Then press 'q'** to exit

### Option 3: Standby Mode (Keep Script Running)

**If you want to recharge Quest but keep script running:**
1. **Move your hands to neutral position** (arms down)
2. **Wait for robot to follow**
3. **Leave script running** (don't exit)
4. **Recharge Quest** (robot will hold position)
5. **Reconnect Quest** when ready

**Note**: Robot will hold current position while script is running (even if Quest disconnected).

## ⚠️ Important Safety Notes

### Before Exiting

According to official docs:
> "To avoid damaging the robot, it is recommended to position the robot's arms close to the initial pose before pressing **q** to exit."

### What "Home Position" Means

- **Home position** = All arm joint angles at zero
- **Neutral pose** = Arms down, elbows bent, hands in front
- The `ctrl_dual_arm_go_home()` function moves arms to zero angles, which should be close to neutral

### If Arms Are Raised

If arms are currently raised:
1. **Move your hands down slowly** to neutral position
2. **Wait 5-10 seconds** for robot to follow (accounting for latency)
3. **Watch robot directly** to confirm arms are moving down
4. **Then press 'q'** to exit

## 🔧 Manual Home Command (If Needed)

If you need to manually return arms to home without exiting:

```python
# In Python (if you have access to arm_ctrl object)
arm_ctrl.ctrl_dual_arm_go_home()
```

But the easiest is just to press **'q'** in the terminal!

## 📋 Exit Process Summary

### Pressing 'q' (Recommended)
1. Arms return to home (~5 seconds)
2. Exits debug mode
3. Clean shutdown

### Pressing Ctrl+C
1. Same as 'q' (script handles it)
2. But 'q' is the intended method

### Leaving Script Running
1. Robot holds current position
2. Safe to disconnect Quest
3. Can reconnect later

## 🎯 Recommended Approach for Recharging

**Best option**: Press **'q'** to safely return arms to neutral, then exit.

**Alternative**: Move hands to neutral, wait for robot, then leave script running while recharging.

