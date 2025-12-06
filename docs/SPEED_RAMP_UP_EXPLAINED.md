# ⚡ Speed Ramp-Up Explained

## What is Speed Ramp-Up?

Speed ramp-up is a **safety feature** that gradually increases the robot's arm movement speed when teleoperation starts. Instead of immediately allowing maximum speed, the robot starts slow and gradually increases to full speed over a few seconds.

## How It Works

### Default Behavior

When you press 'r' to start teleoperation, the script calls:
```python
arm_ctrl.speed_gradual_max()
```

This activates the speed ramp-up feature with these parameters:

- **Initial Speed**: `20.0` (rad/s velocity limit)
- **Maximum Speed**: `30.0` (rad/s velocity limit)
- **Ramp-Up Time**: `5.0` seconds (default)
- **Formula**: `speed = 20.0 + (10.0 * min(1.0, elapsed_time / 5.0))`

### Speed Progression

| Time (seconds) | Speed (rad/s) | Percentage |
|----------------|---------------|------------|
| 0.0            | 20.0          | 67%        |
| 1.0            | 22.0          | 73%        |
| 2.0            | 24.0          | 80%        |
| 3.0            | 26.0          | 87%        |
| 4.0            | 28.0          | 93%        |
| 5.0+           | 30.0          | 100%       |

### Why It Exists

1. **Safety**: Prevents sudden, jerky movements when starting
2. **Stability**: Allows robot to stabilize before full-speed operation
3. **User Experience**: Gives operator time to adjust and align
4. **Error Prevention**: Reduces risk of overshooting or collisions

## Customizing Speed Ramp-Up

### Change Ramp-Up Time

You can modify the ramp-up time by editing `teleop_hand_and_arm.py`:

```python
# Current (5 seconds):
arm_ctrl.speed_gradual_max()

# Faster (3 seconds):
arm_ctrl.speed_gradual_max(t=3.0)

# Slower (10 seconds):
arm_ctrl.speed_gradual_max(t=10.0)
```

### Disable Ramp-Up (Instant Max Speed)

If you want to skip the ramp-up and go straight to maximum speed:

```python
# In teleop_hand_and_arm.py, replace:
arm_ctrl.speed_gradual_max()

# With:
arm_ctrl.speed_instant_max()
```

**⚠️ Warning**: Instant max speed can cause jerky movements and is less safe!

## Code Location

The speed ramp-up logic is in:
- **File**: `dependencies/xr_teleoperate/teleop/robot_control/robot_arm.py`
- **Method**: `speed_gradual_max(t=5.0)` (line ~585)
- **Implementation**: `ctrl_dual_arm()` method (line ~531)

### Key Code Snippet

```python
def speed_gradual_max(self, t = 5.0):
    '''Parameter t is the total time required for arms velocity to gradually increase to its maximum value, in seconds. The default is 5.0.'''
    self._gradual_start_time = time.time()
    self._gradual_time = t
    self._speed_gradual_max = True

# In ctrl_dual_arm():
if self._speed_gradual_max is True:
    t_elapsed = start_time - self._gradual_start_time
    self.arm_velocity_limit = 20.0 + (10.0 * min(1.0, t_elapsed / 5.0))
```

## Impact on Control

### During Ramp-Up (0-5 seconds)
- **Movement feels slow** - This is normal!
- **Robot may lag behind** - Especially for large movements
- **Control feels less responsive** - Speed is intentionally limited

### After Ramp-Up (5+ seconds)
- **Full speed available** - 30.0 rad/s velocity limit
- **More responsive** - Robot can move faster
- **Better correlation** - Movements match your hands better

## Recommendations

### For Testing
- **Keep default (5 seconds)** - Safe and stable
- **Watch robot directly** - See the speed increase
- **Make slow movements initially** - Let speed ramp up

### For Production
- **Keep default** - Safety is important
- **Only disable if needed** - And only if you're experienced
- **Consider longer ramp-up** - If robot is unstable

## Troubleshooting

### "Robot feels too slow"
- **Wait 5 seconds** - Speed will increase
- **Check ramp-up is working** - Should see gradual improvement
- **Make larger movements** - Easier to see at lower speeds

### "Robot still slow after 5 seconds"
- **Check velocity limit** - Should be 30.0 after ramp-up
- **Verify ramp-up completed** - Check logs for speed values
- **Consider instant max** - Only if you understand the risks

### "Want faster ramp-up"
- **Reduce time parameter** - `speed_gradual_max(t=3.0)`
- **Or disable entirely** - `speed_instant_max()`

## Summary

- ✅ **Speed ramp-up is a safety feature** - Starts slow, increases gradually
- ✅ **Default: 5 seconds** - From 20.0 to 30.0 rad/s
- ✅ **Normal behavior** - Robot will feel slow initially
- ✅ **Customizable** - Can adjust time or disable
- ⚠️ **Be patient** - Wait 5 seconds for full speed

