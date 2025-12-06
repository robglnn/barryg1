# Controller Freeze Fix

## Problem

After extended use (6+ minutes), the robot arms can "freeze" in place and stop responding to Quest controller movements. The controller positions remain frozen at the last valid pose.

## Root Cause

The issue is caused by a **pose data size mismatch** in the controller event handler. When the Quest browser sends controller pose data in an unexpected format (not exactly 16 elements for a 4x4 matrix), the assignment fails with:

```
ValueError: Can only assign sequence of same size
```

This causes the controller pose data to stop updating, making the robot appear "locked" even though controllers are still being tracked.

## Solution

Added robust pose data validation and conversion in `televuer.py`:

1. **Size Validation**: Checks if incoming pose data is exactly 16 elements (4x4 matrix)
2. **Format Conversion**: Handles 12-element (3x4) matrices by padding to 4x4
3. **Error Handling**: Skips invalid updates instead of crashing, preserving the last valid pose
4. **Logging**: Warns about size mismatches (first 10 occurrences) to help diagnose issues

## Prevention

The fix prevents the freeze by:
- Validating pose data size before assignment
- Gracefully handling format mismatches
- Preserving the last valid pose when invalid data is received
- Continuing to process subsequent valid updates

## Recovery

If the robot freezes:
1. **Move controllers back to a neutral position** - This may trigger a valid pose update
2. **Press 'q' to safely exit** - This returns arms to home position
3. **Restart teleoperation** - The fix should prevent future freezes

## Additional Notes

- The robot's IK solver has joint limits (`lowerPositionLimit`, `upperPositionLimit`)
- The arm controller uses velocity limiting (`clip_arm_q_target`) to prevent sudden movements
- If joints approach limits, the IK solver may fail to find a solution, but this shouldn't cause a freeze
- The freeze is specifically caused by the pose data format mismatch, not joint limits

