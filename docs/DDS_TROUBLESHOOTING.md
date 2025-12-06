# 🔧 DDS Connection Troubleshooting

## Current Issue

Robot is in Debug Mode (L2+R2, then L2+A), but script still shows:
- `Enter debug mode: Failed`
- `[G1_23_ArmController] Waiting to subscribe dds...`

## Root Cause

The robot's **low-level DDS service** needs to be active on PC2. According to Unitree SDK documentation:

> **"First, use the app to turn off the high-level motion service (sport_mode) to prevent conflicting instructions."**

This means:
1. The robot's **high-level motion service** must be **disabled** on PC2
2. The robot's **low-level DDS service** must be **running** on PC2
3. The robot must be in **Debug Mode** (which you've done)

## What Needs to Run on Robot PC2

### Required Services:

1. **Low-level DDS service** - Must be running (this publishes `rt/lowstate` topic)
2. **High-level motion service** - Must be **DISABLED** (to prevent conflicts)

### How to Check/Configure on PC2:

**Option 1: Use Robot App**
- Open the Unitree robot control app
- **Disable/Turn off** the high-level motion service (sport_mode)
- Ensure low-level service is active

**Option 2: SSH into PC2**
```bash
# SSH into robot's PC2
ssh unitree@192.168.123.164

# Check if services are running
# (exact commands depend on robot's OS setup)
```

## Why "Enter debug mode: Failed"

The `MotionSwitcher.Enter_Debug_Mode()` function:
1. Checks current mode via DDS
2. Releases any active mode
3. Enters debug mode

If it fails, it could mean:
- DDS communication isn't working (robot's DDS service not running)
- Robot is in a mode that can't be released
- Network/DDS configuration issue

## Solutions to Try

### Solution 1: Disable High-Level Service on Robot

1. **On robot's PC2 or via app**: Disable high-level motion service
2. **Restart the teleoperation script**
3. The script should now be able to enter debug mode

### Solution 2: Check DDS Environment Variables

On your Mac, ensure DDS is configured:
```bash
# Check if CYCLONEDDS_HOME is set
echo $CYCLONEDDS_HOME

# If not set, you may need to set it (though it should work without it)
```

### Solution 3: Test DDS Connection Directly

Try running a simple DDS test from your Mac:
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop
cd ~/unitree_sdk2_python/example/low_level
python3 lowlevel_control.py <network_interface>
```

This will test if you can receive low-level state data from the robot.

### Solution 4: Check Robot's Network Interface

The robot's PC2 needs to be publishing DDS on the correct network interface. Verify:
- Robot is on 192.168.123.X network
- Robot's DDS service is bound to the correct interface
- No firewall blocking DDS ports

## Expected Behavior When Working

When everything is configured correctly, you should see:
1. `Enter debug mode: Success` (or it detects you're already in debug mode)
2. `[G1_23_ArmController] Subscribe dds ok.` (within a few seconds)
3. Script proceeds to wait for 'r' key press

## Next Steps

1. **Check robot's app/PC2** - Disable high-level motion service
2. **Verify robot's DDS service is running** on PC2
3. **Wait 30-60 seconds** after putting robot in debug mode (DDS may need time to initialize)
4. **Restart the teleoperation script**

The key issue is likely that the robot's high-level motion service is still running, preventing the low-level DDS from working properly.

