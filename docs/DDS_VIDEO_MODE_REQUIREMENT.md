# 🔧 DDS Video Mode Requirement

## Error Code 3102: RPC_ERR_CLIENT_SEND

**Error**: `[ClientStub] send request error. id: 139971566063916`  
**Code**: `3102`  
**Meaning**: `RPC_ERR_CLIENT_SEND` - The RPC request couldn't be sent/received

## Root Cause

The **video service** on the robot requires the robot to be in **Debug Mode**, not Zero Torque Mode.

## Solution

### Put Robot in Debug Mode

1. **On robot remote control:**
   - Press **L2 + R2** simultaneously
   - Then press **L2 + A**
   - Robot should beep/indicate it's in Debug Mode

2. **Verify Debug Mode:**
   - Robot should be responsive but not moving
   - DDS connection should work (robot control works)

3. **Run test again:**
   ```bash
   source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1 && python test_dds_video.py en7
   ```

## Why Debug Mode?

- **Zero Torque Mode**: Robot motors are disabled, but services may not be fully active
- **Debug Mode**: All low-level services are active, including video service
- **Video Service**: Part of the robot's RPC services, requires Debug Mode to be available

## Expected Behavior After Debug Mode

✅ DDS initialized successfully  
✅ VideoClient initialized successfully  
✅ **Video frames received** (not error code 3102)  
✅ OpenCV window showing robot camera feed  
✅ Frame count increasing  

## Note

The teleoperation script automatically puts the robot in Debug Mode, so when you run full teleoperation, video should work. But for standalone video testing, you need to manually put the robot in Debug Mode first.

