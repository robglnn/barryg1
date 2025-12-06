# ⚠️ Why 'r' Key Doesn't Work - DDS Blocking Issue

## The Problem

The script is **stuck waiting for DDS connection** before it can even listen for the 'r' key. The main loop is blocked at:

```
[G1_23_ArmController] Waiting to subscribe dds...
```

Until DDS connects, the script won't proceed to the point where it waits for keyboard input ('r' key).

## Why 'r' Does Nothing

1. Script initializes
2. Script tries to connect to robot via DDS
3. **Script gets stuck here** - waiting for DDS data
4. Script never reaches the keyboard listener part
5. Pressing 'r' has no effect because the script is blocked

## Solution: Fix DDS Connection First

The robot's PC2 must be publishing DDS data. The script subscribes to `rt/lowstate` topic.

### Check Robot Side

**On robot's PC2, you need:**
1. **Low-level DDS service running** - This publishes robot state
2. **High-level motion service DISABLED** - Prevents conflicts
3. **Robot in Debug Mode** - Required for low-level control

### Verify DDS is Working

Try the DDS test command (now that timerfd is fixed):

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/unitree_sdk2_python/example/g1/low_level && python3 g1_low_level_example.py en7
```

If this also shows "Waiting to subscribe dds...", then:
- Robot's DDS service is not running
- Robot's PC2 is not publishing on `rt/lowstate` topic
- Network/DDS configuration issue

### What to Check on Robot

1. **Robot App/PC2**: 
   - Disable high-level motion service
   - Ensure low-level DDS service is active
   - Verify robot is in Debug Mode

2. **Robot Network**:
   - Robot should be on 192.168.123.164
   - DDS should be configured for this network interface
   - No firewall blocking DDS ports

3. **Robot Software**:
   - PC2 should be running compatible software
   - DDS service should be initialized

## Alternative: Test Without Robot

If you just want to test the VR interface without robot control:
- The script won't proceed without DDS
- You'd need to modify the code to skip DDS wait (not recommended)
- Better to fix DDS connection first

## Next Steps

1. **Check robot's PC2** - Is DDS service running?
2. **Run DDS test command** - Does it connect?
3. **Verify robot network** - Is it on correct network?
4. **Check robot mode** - Is it in Debug Mode?

Once DDS connects, you'll see:
```
[G1_23_ArmController] Subscribe dds ok.
```

Then the script will proceed and 'r' key will work!

