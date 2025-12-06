# 🎮 VR Black Screen - What to Do Next

## Current Status

✅ Server is running (port 8012 working)
✅ Quest connected to VR
⚠️ Black screen (normal - waiting for teleoperation to start)
⚠️ Robot DDS not connected yet ("Waiting to subscribe dds...")

## What Should Happen

### Step 1: Wait for Robot DDS Connection

The script is still waiting for the robot:
```
[G1_23_ArmController] Waiting to subscribe dds...
```

**You need to:**
1. Make sure robot's PC2 DDS service is running
2. Ensure robot is in Debug Mode (L2+R2, then L2+A)
3. Wait for the message: `[G1_23_ArmController] Subscribe dds ok.`

### Step 2: Press 'r' in Terminal

Once DDS connects (or even before, to test), **press 'r' in the terminal** where the script is running.

This starts teleoperation mode. You should see:
- Terminal message about starting teleoperation
- VR screen should show robot's camera feed (if camera is configured)
- Your hand movements should start controlling the robot

### Step 3: What You Should See in VR

**Expected:**
- Robot's first-person camera view (from robot's head camera)
- Your virtual hands in VR space
- Robot's hands/arms moving as you move your hands

**If still black screen:**
- Camera feed may not be configured on robot PC2
- Image service (teleimager) may not be running on robot
- Check robot's camera is working

### Step 4: Hand Tracking

**Your hands should:**
- Be tracked by Quest 3 (you'll see virtual hands)
- Control robot's arms when you move them
- Control robot's hands when you make gestures

**If hands not working:**
- Make sure Quest hand tracking is enabled
- Check Quest settings → Hand Tracking
- Try moving hands slowly at first

## Troubleshooting Black Screen

### Issue 1: Robot Not Connected
- **Symptom**: Still seeing "Waiting to subscribe dds..."
- **Fix**: Check robot's PC2 DDS service is running

### Issue 2: Camera Feed Not Working
- **Symptom**: Black screen even after pressing 'r'
- **Fix**: 
  - Check robot's camera is connected
  - Verify teleimager service is running on robot PC2
  - Check `192.168.123.164:60001` in browser (should show camera feed)

### Issue 3: Pressed 'r' But Nothing Happens
- **Symptom**: Pressed 'r' but still black screen
- **Fix**: 
  - Make sure you're pressing 'r' in the terminal (not in VR)
  - Wait for DDS connection first
  - Check terminal for error messages

## Next Steps

1. **Wait for DDS connection** (or proceed if robot is ready)
2. **Press 'r' in terminal** to start teleoperation
3. **Move your hands** - robot should respond
4. **Check camera feed** - should see robot's perspective

## Quick Test

Try pressing 'r' in the terminal now (even if DDS isn't connected). You should see:
- Terminal message: "Starting teleoperation..." or similar
- VR may still be black if camera feed isn't working, but hand tracking should work

