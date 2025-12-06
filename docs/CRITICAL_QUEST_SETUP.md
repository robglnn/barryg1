# ⚠️ CRITICAL: Quest Controller Setup

## The Problem

You're seeing the browser interface, which means you're **NOT in VR mode**. Controllers **ONLY work in VR mode**, not in browser mode.

## The Solution

### Step-by-Step:

1. **Open Quest Browser** to `https://192.168.123.56:8012`
2. **Look for "Virtual Reality" button** at the bottom of the browser
3. **Click "Virtual Reality" button** - This enters VR mode
4. **You should now see the robot's camera view in VR** (not browser)
5. **Controllers should appear** - You'll see your Quest controllers in VR space
6. **Move controllers** - They should now control the robot arms
7. **Move joysticks** - They should now control locomotion

### What You're Seeing Now:

- **Browser mode**: Shows one camera view, controllers don't work
- **Mouse/Keyboard controls**: The "red green blue XYZ" you mentioned - this is browser mode
- **G1 controller works**: Because it's direct DDS, not dependent on VR mode

### What You Need:

- **VR mode**: Click "Virtual Reality" button
- **Controllers visible**: You should see Quest controllers in VR
- **Then controllers work**: Arm control and joystick locomotion will work

## Verification

After entering VR mode, check the logs for:
```
[TeleVuer] ✅ Controller event #1 received!
[TeleVuer] ✅ First controller event processed!
[tv_wrapper] Controller validity - Left: True, Right: True
[Controller Debug] Left thumbstick: [...], Right thumbstick: [...]
```

If you DON'T see these messages, controllers aren't being tracked.

## About Stereo Video

- **Browser preview**: Shows one eye (this is normal)
- **VR mode**: Shows proper stereo (left/right eyes separated)
- The `layers=1` and `layers=2` parameters separate left/right eyes in VR
- In browser, they may appear to overlap, but in VR they're correctly separated

## Summary

**You MUST click "Virtual Reality" button to enter VR mode for controllers to work!**

Browser mode = No controllers
VR mode = Controllers work

