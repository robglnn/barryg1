# 🔌 Robot Power and Port Requirements

## Port 60000 Timeout (Not a Problem)

**What it is:** Camera configuration server (teleimager)
- **Port:** 60000
- **Purpose:** Gets camera settings from robot's PC2
- **Timeout message:** `Request to 192.168.123.164:60000 timed out or no response, using local config.`

**Is it a problem?** **NO** - The script automatically falls back to local config file:
- Uses: `/Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop/teleimager/cam_config_server.yaml`
- This is fine for teleoperation - camera feed will still work

**When it works:** Only when robot's PC2 has teleimager service running (optional)

## DDS Connection (Requires Robot Power)

**What it is:** Data Distribution Service for robot control
- **Port:** DDS uses multicast (not a single port)
- **Purpose:** Real-time communication with robot (motor states, commands)
- **Error:** `[Reader] take sample error` means robot isn't responding

**Is it a problem?** **YES** - Can't control robot without DDS connection

**Requirements:**
1. ✅ Robot must be **powered on**
2. ✅ Robot must be in **Debug Mode** (L2+R2, then L2+A)
3. ✅ Robot's PC2 must have **DDS service running**
4. ✅ Network connection (Mac ↔ Robot on 192.168.123.X)

## Current Status

Based on your output:
- ❌ **Robot is OFF** → DDS can't connect
- ⚠️ **Port 60000 timeout** → Not a problem (using local config)
- ✅ **DDS initialization** → Working correctly (`DDS initialized with network interface: en7`)

## What to Do

1. **Turn robot ON**
2. **Put robot in Debug Mode:**
   - Press L2+R2 simultaneously
   - Then press L2+A
   - Robot should beep/indicate debug mode
3. **Run the script again**

The script is working correctly - it just needs the robot to be powered on and in debug mode!

