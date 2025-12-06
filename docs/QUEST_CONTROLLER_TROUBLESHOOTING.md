# Quest Controller Troubleshooting

## Current Issue
Quest controllers are connected (websocket connections visible) but no arm or leg movements are happening.

## Debug Logs Added

The code now includes extensive debug logging. You should see:

### 1. Controller Event Reception
When controllers move, you should see:
```
[TeleVuer] ✅ Controller event received! Left: True, Right: True
[TeleVuer] Left thumbstick: [...]
[TeleVuer] Right thumbstick: [...]
```

**If you DON'T see this**: Controllers aren't sending events from Quest browser.

### 2. Controller Data Validity
Every second, you should see:
```
[tv_wrapper] Controller validity - Left: True, Right: True
[tv_wrapper] Left thumbstick: [...], Right thumbstick: [...]
[tv_wrapper] Left A button: False, Right A button: False
```

**If validity is False**: Controllers aren't being tracked properly.

### 3. Main Loop Controller Debug
Every second, you should see:
```
[Controller Debug] Left wrist pos: [...], Right wrist pos: [...]
[Controller Debug] Left thumbstick: [...], Right thumbstick: [...]
[Controller Debug] Left A button: False, Right A button: False
```

**If positions are all zeros/constant**: Controllers not being read.

### 4. Locomotion Commands
When joysticks are moved, you should see:
```
[Locomotion] Sending command: vx=0.123, vy=0.045, vyaw=0.067
```

**If you DON'T see this**: Joystick values aren't being read.

## Common Issues and Fixes

### Issue 1: No Controller Events Received
**Symptoms**: No `[TeleVuer] ✅ Controller event received!` messages

**Possible Causes**:
1. Quest browser not in VR mode
2. Controllers not paired/tracked
3. Quest browser permissions not granted

**Fixes**:
- Make sure you clicked "Enter VR" in the Quest browser
- Check that controllers are visible in VR space
- Try re-pairing controllers
- Check Quest browser console for errors (if accessible)

### Issue 2: Controller Events Received but Data Invalid
**Symptoms**: See `[TeleVuer] ✅ Controller event received!` but validity is False

**Possible Causes**:
1. Controllers not properly initialized
2. Controller pose data malformed
3. Shared memory not being updated

**Fixes**:
- Try moving controllers - they should appear in VR
- Check if controllers are visible in the VR scene
- Restart teleoperation script

### Issue 3: Controller Data Valid but Robot Doesn't Move
**Symptoms**: See valid controller data but robot doesn't respond

**Possible Causes**:
1. Robot not in correct mode (should be Motion Mode for locomotion)
2. DDS commands not being sent
3. Arm controller using wrong DDS topic

**Fixes**:
- Verify robot is in Motion Mode (R1+X)
- Check DDS connection logs
- Verify `loco_wrapper` is initialized (should see "LocoClientWrapper initialized")

## Next Steps

1. **Restart teleoperation** and watch for the debug logs
2. **Move Quest controllers** and check if events are received
3. **Move joysticks** and check if thumbstick values change
4. **Share the log output** so we can identify the exact issue

## Expected Log Flow

When everything works:
1. Quest connects → `websocket is connected`
2. Controllers move → `[TeleVuer] ✅ Controller event received!`
3. Data processed → `[Controller Debug] Left thumbstick: [0.5, 0.3]`
4. Commands sent → `[Locomotion] Sending command: vx=0.15, vy=0.09, vyaw=0.0`
5. Robot moves

If any step is missing, that's where the issue is.

