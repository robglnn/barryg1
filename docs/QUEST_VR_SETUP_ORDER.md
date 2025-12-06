# 🎮 Quest VR Setup Order

## Recommended Order

### Step 1: Connect Quest Browser
1. **Open Quest Browser** (not regular browser)
2. **Navigate to**: `https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012`
3. **Accept SSL warning** (click "Advanced" → "Proceed")
4. You should see a UI with buttons

### Step 2: Enter VR Mode (BEFORE pressing 'r')
1. **Click "Virtual Reality" button** in Quest Browser
2. This enters VR mode (you'll see black screen - this is normal)
3. You're now in VR, ready for teleoperation

### Step 3: Press 'r' in Terminal
1. **Look at your Mac terminal** (not VR)
2. **Press 'r' key**
3. You should see: `---------------------🚀start program🚀-------------------------`
4. **Now teleoperation starts!**

## Why This Order?

- **Enter VR first**: Gets you into VR mode and ready
- **Then press 'r'**: Starts the teleoperation loop, which begins:
  - Hand tracking data collection
  - Robot control commands
  - Camera feed streaming (if configured)

## What You'll See

### Before pressing 'r':
- ✅ Quest in VR mode (black screen is normal)
- ✅ Terminal waiting: `Please enter the start signal (enter 'r' to start...)`
- ✅ Robot arms locked in current position

### After pressing 'r':
- ✅ Terminal shows: `---------------------🚀start program🚀-------------------------`
- ✅ VR should show robot camera feed (if camera is configured)
- ✅ Robot should respond to your hand movements
- ✅ If camera not configured, VR may still be black but hand tracking works

## Alternative: Press 'r' First

You can also:
1. Press 'r' in terminal first
2. Then enter VR mode in Quest

**But it's better to enter VR first** so you're ready when teleoperation starts.

## Pass Through Mode

- **"Pass Through"** shows the real world with VR overlay
- Use this if you want to see your actual hands/room
- **"Virtual Reality"** is full VR immersion (recommended for teleoperation)

## Summary

**Recommended**: Enter VR mode → Press 'r' → Start teleoperating! 🚀

