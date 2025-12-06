# Quest Controller Setup Guide

## Critical: Controllers Only Work in VR Mode

**Quest controllers will NOT send data unless the browser is in VR mode!**

### Steps to Enable Controllers:

1. **Open Quest Browser** to `https://192.168.123.56:8012`
2. **Click "Virtual Reality" button** at the bottom of the browser
3. **Enter VR mode** - You should see the robot's camera view in VR
4. **Controllers should appear** - You should see your Quest controllers visible in the VR space
5. **Move controllers** - They should track your hand movements

### If Controllers Don't Appear:

1. **Check Quest controller batteries** - Low batteries can prevent tracking
2. **Re-pair controllers** - Go to Quest Settings > Controllers > Pair new controller
3. **Restart Quest** - Sometimes a restart helps with controller tracking
4. **Check Quest Guardian** - Make sure Guardian is set up and controllers are within tracking area
5. **Try different lighting** - Poor lighting can affect controller tracking

### Verification:

When controllers are working, you should see in the logs:
```
[TeleVuer] ✅ Controller event #1 received!
[TeleVuer] ✅ First controller event processed! Left controller: True, Right controller: True
[tv_wrapper] Controller validity - Left: True, Right: True
[tv_wrapper] Left thumbstick: [...], Right thumbstick: [...]
[Controller Debug] Left wrist pos: [...], Right wrist pos: [...]
```

### Browser vs VR Mode:

- **Browser mode**: Controllers don't work - you can only use mouse/keyboard
- **VR mode**: Controllers work - you can use Quest controllers for arm control and joysticks for locomotion

### Common Issues:

1. **"Only seeing one eye" in browser**: This is normal - browser preview shows one view. In VR, you'll see proper stereo.
2. **"Controllers not working"**: Make sure you clicked "Virtual Reality" button and entered VR mode
3. **"Arm control from browser XYZ"**: This is mouse/keyboard control, not Quest controllers. Enter VR mode for Quest controllers.

