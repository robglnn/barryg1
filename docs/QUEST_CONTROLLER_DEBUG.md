# Quest Controller Debugging Guide

## Issue: Quest Controllers Not Controlling Robot

### Symptoms
- Video streaming works
- Robot is in Motion Mode (R1+X) - confirmed by handheld controller working
- Quest controllers are not moving arms or legs
- Locomotion commands not being sent

### Debugging Steps

1. **Check if controllers are being tracked in Quest browser:**
   - In VR mode, you should see the Quest controllers visible in the VR space
   - If controllers are not visible, they may not be tracked
   - Try moving controllers - they should appear in VR

2. **Check debug logs:**
   The teleoperation script now logs controller data every second:
   ```
   [Controller Debug] Left wrist pos: [...], Right wrist pos: [...]
   [Controller Debug] Left thumbstick: [...], Right thumbstick: [...]
   [Controller Debug] Left A button: False, Right A button: False
   ```

3. **What to look for:**
   - If wrist positions are all zeros or constant: Controllers not being tracked
   - If thumbstick values are all zeros: Joysticks not being read
   - If positions are changing: Controllers are tracked, issue is in command sending

4. **Common Issues:**
   - **Controllers not visible in VR**: Quest controllers may need to be re-paired or batteries replaced
   - **Quest browser not in VR mode**: Make sure you clicked "Enter VR" in the browser
   - **Controllers not enabled**: Some Quest browsers require explicit permission for controller tracking

### Fixes Applied

1. **Added debug logging** to `teleop_hand_and_arm.py`:
   - Logs controller positions every second
   - Logs thumbstick values
   - Logs button states
   - Logs locomotion commands when non-zero

2. **Controller data flow:**
   - Quest Browser → Vuer Server → `on_controller_move` event → Shared Memory → `get_tele_data()` → Robot commands

### Next Steps

1. Run teleoperation and check the logs for controller debug output
2. If controller positions are zeros/constant: Controllers not being tracked
3. If positions are changing but robot doesn't move: Issue in command sending (check DDS/Motion Mode)
4. If thumbstick values are zeros: Joysticks not being read (check Quest controller state)

