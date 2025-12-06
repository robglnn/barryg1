# 🤲 Hand Tracking Control Explained

## How Control Works (Hand Tracking Mode)

You're using `--input-mode=hand`, which means:

### ✅ What Controls the Robot

**Your WRIST position and orientation** → Robot arm position and orientation

- **Left wrist pose** (position + rotation) → Left robot arm
- **Right wrist pose** (position + rotation) → Right robot arm
- **NOT controller position** (that's for `--input-mode=controller`)
- **NOT joysticks** (those are for controller mode with motion)
- **NOT buttons** (those are for controller mode)

### How It Works

1. **Quest 3 tracks your hands** → Gets wrist position and orientation
2. **Vuer sends wrist poses** → Via WebSocket to Mac
3. **Inverse Kinematics (IK) solver** → Converts wrist poses to robot joint angles
4. **Robot arms move** → To match your wrist positions

### What "Wrist Pose" Means

- **Position**: X, Y, Z coordinates of your wrist
- **Orientation**: How your wrist is rotated (pitch, roll, yaw)

## 🎮 Controller vs Hand Mode

### Hand Tracking Mode (`--input-mode=hand`) ← **You're using this**
- **Input**: Your actual hand/wrist positions
- **Controls**: Robot arm position and orientation
- **Hand gestures**: Control robot hands (if end-effector configured)

### Controller Mode (`--input-mode=controller`)
- **Input**: Quest controllers
- **Controls**: 
  - Joysticks → Robot movement (if `--motion` enabled)
  - Buttons → Various functions
  - Controller position → Robot arm position

## 🧪 Tests to Make Control Clearer

### Test 1: Large Movements
1. **Start with arms at sides**
2. **Raise left hand straight up** (slowly)
3. **Watch robot** → Left arm should raise
4. **Lower left hand** → Robot arm should lower
5. **Repeat with right hand**

### Test 2: One Arm at a Time
1. **Keep right arm still** (at side)
2. **Move only left arm** (up, down, forward, back)
3. **Watch robot** → Only left arm should move
4. **Switch** → Move only right arm

### Test 3: Forward/Back Movement
1. **Start with arms in front**
2. **Move hands forward** (away from body)
3. **Robot arms should extend forward**
4. **Move hands back** (toward body)
5. **Robot arms should retract**

### Test 4: Rotation Test
1. **Hold arm straight out**
2. **Rotate your wrist** (twist it)
3. **Robot wrist should rotate**

### Test 5: Position Verification
1. **Stand in front of robot**
2. **Match your arm position to robot's**
3. **Move your arms slowly**
4. **Robot should follow with slight delay**

## 🔍 Why Control Feels Unclear

### Latency (~50-100ms)
- Normal for WiFi + processing
- Makes it hard to see direct correlation
- **Solution**: Make larger, slower movements

### No Visual Feedback
- Black screen in VR (until camera feed)
- Can't see robot's perspective
- **Solution**: Watch robot directly

### Speed Ramp-Up
- Robot starts slow for safety
- Gradually increases speed
- **Solution**: Wait 5-10 seconds after starting

### Initial Position Mismatch
- Your arms might not match robot's position
- Robot tries to match your position
- **Solution**: Align arms before pressing 'r'

## 💡 Tips for Better Control

1. **Start aligned** → Match robot's initial pose before 'r'
2. **Large movements** → Easier to see correlation
3. **One arm at a time** → Clearer feedback
4. **Watch robot directly** → Visual confirmation
5. **Slow and deliberate** → Better control
6. **Be patient** → Latency is normal

## 🎯 What to Expect

### When Control is Working
- ✅ Robot arms follow your hand movements (with delay)
- ✅ Smooth, controlled motion
- ✅ No sudden jerky movements
- ✅ Terminal shows continuous IK solving

### When Control Isn't Working
- ❌ Robot doesn't move at all
- ❌ Jerky, unstable movement
- ❌ Arms stuck at limits
- ❌ Terminal shows errors

## 📊 Understanding the Data Flow

```
Quest 3 Hand Tracking
    ↓ (Tracks your hands)
Wrist Position + Orientation
    ↓ (WebSocket to Mac)
Vuer Server
    ↓ (Extracts wrist poses)
Inverse Kinematics Solver
    ↓ (Calculates joint angles)
Robot Arm Control
    ↓ (DDS commands)
Robot Motors
```

## 🎮 Summary

**You're using HAND TRACKING mode:**
- ✅ **Wrist position** → Robot arm position
- ✅ **Wrist rotation** → Robot wrist rotation
- ❌ **NOT joysticks** (those are for controller mode)
- ❌ **NOT buttons** (those are for controller mode)
- ❌ **NOT controller position** (that's controller mode)

**Make large, slow movements and watch the robot directly to see the correlation!**

