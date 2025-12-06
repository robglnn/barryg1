# 🎮 Quest 3 Usage Guide for XR Teleoperation

## 🎯 Which VR Button to Use?

### ✅ Use the "Virtual Reality" Button in the Vuer UI

**Location**: Inside the Vuer web page (the page you loaded in Quest Browser)

**NOT**: The browser's "Enter VR" button in the upper right corner (that's a browser feature, not for teleoperation)

**When**: Click "Virtual Reality" button **BEFORE** pressing 'r' in terminal

## 📋 Complete Setup Order

1. **Load Quest Browser** → Navigate to `https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012`
2. **Accept SSL warning** → Click "Advanced" → "Proceed"
3. **Click "Virtual Reality" button** in the Vuer UI (not browser's "Enter VR")
4. **Allow all prompts** → Grant permissions for VR session
5. **Press 'r' in terminal** → Starts teleoperation

## 🤲 How Hand Tracking Works

### What Controls the Robot

**Your wrist position and orientation** → Controls robot arm position and orientation

The system uses:
- **Left wrist pose** → Left robot arm
- **Right wrist pose** → Right robot arm
- **Inverse Kinematics (IK)** → Converts wrist poses to robot joint angles

### Hand Movements → Robot Movements

- **Move your left hand up/down/forward/back** → Left robot arm follows
- **Move your right hand up/down/forward/back** → Right robot arm follows
- **Rotate your wrists** → Robot wrists rotate
- **Hand gestures** → Control robot hands (if you have end-effectors like Dex3)

### Initial Alignment (IMPORTANT!)

**Before pressing 'r'**, align your arms to match the robot's initial pose:

```
Robot Initial Pose:
- Arms slightly down and forward
- Elbows bent
- Hands in front of body
```

**Why**: Avoids sudden movements when teleoperation starts. The robot arms should match your arm position.

## ⚡ Latency and Feedback

### Expected Latency

- **Network latency**: ~10-50ms (WiFi)
- **Processing latency**: ~30-50ms (IK solving, DDS communication)
- **Total**: ~50-100ms from hand movement to robot response

### Why It Might Feel Unclear

1. **No visual feedback in VR** (black screen until camera feed starts)
2. **Robot arms might be in different position** than your arms initially
3. **Latency makes it hard to see direct correlation**
4. **Robot might be moving slowly** (gradual speed ramp-up for safety)

### How to Verify It's Working

1. **Make large, slow movements** → Robot should follow
2. **Watch the robot directly** (not just in VR) → See if arms move
3. **Move one hand at a time** → Easier to see correlation
4. **Check terminal** → Should show IK solving and control commands

## 🎮 Controls Summary

### Hand Tracking Mode (`--input-mode=hand`)

| Your Action | Robot Response |
|------------|----------------|
| Move left wrist | Left arm moves |
| Move right wrist | Right arm moves |
| Rotate wrists | Robot wrists rotate |
| Hand gestures | Robot hands (if end-effector configured) |

### Keyboard Controls (Terminal)

- **'r'** → Start teleoperation
- **'s'** → Start/stop recording (if `--record` enabled)
- **'q'** → Quit teleoperation

## 🔍 Troubleshooting

### Arms Don't Move

1. **Check if 'r' was pressed** → Terminal should show `🚀start program🚀`
2. **Check hand tracking** → Make sure hands are visible to Quest cameras
3. **Check alignment** → Arms might be at limits
4. **Check terminal for errors** → Look for IK or control errors

### Arms Move But Not Responsive

1. **Latency is normal** → 50-100ms delay is expected
2. **Speed ramp-up** → Robot starts slow for safety
3. **Make larger movements** → Small movements might not be noticeable
4. **Check network** → WiFi latency affects responsiveness

### Black Screen in VR

- **Before 'r'**: Normal (waiting for teleoperation to start)
- **After 'r'**: 
  - Camera feed may not be configured
  - Check if robot's teleimager service is running
  - Hand tracking should still work even without camera feed

## 📊 Understanding the System

### Data Flow

```
Quest 3 Hand Tracking
    ↓ (WebSocket)
Mac (Vuer Server)
    ↓ (Process hand poses)
Inverse Kinematics Solver
    ↓ (Calculate joint angles)
DDS Command Publisher
    ↓ (Cyclone DDS)
Robot PC2
    ↓ (Low-level control)
Robot Motors
```

### What You're Controlling

- **Wrist poses** (position + orientation) → Converted to 10 joint angles (5 per arm)
- **Hand gestures** → Converted to hand motor commands (if end-effector configured)

## 💡 Tips for Better Control

1. **Start with arms aligned** → Match robot's initial pose before pressing 'r'
2. **Make slow, deliberate movements** → Easier to see correlation
3. **Move one arm at a time** → Better feedback
4. **Watch the robot directly** → Visual feedback helps
5. **Be patient** → Latency and speed ramp-up are normal

## 🎯 Expected Behavior

### When It's Working Correctly

- ✅ Robot arms follow your hand movements (with slight latency)
- ✅ Smooth, controlled motion
- ✅ No sudden jerky movements
- ✅ Terminal shows continuous IK solving

### When Something's Wrong

- ❌ Robot doesn't move at all → Check 'r' was pressed, check terminal errors
- ❌ Jerky, unstable movement → Check network, check robot state
- ❌ Arms stuck at limits → Move your arms to different position

## 📚 Reference

- **Official Docs**: See `dependencies/xr_teleoperate/README.md`
- **Initial Pose**: Arms slightly down, elbows bent, hands in front
- **Control Frequency**: 30 Hz (default, can be changed with `--frequency`)

