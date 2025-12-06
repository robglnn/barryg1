# Active Context: XR Teleoperation Setup

## Current Work Focus

**✅ Stable Arm Control with Visual Passthrough to Quest VR Achieved!**

The system is now stable and operational:
- Quest controllers control robot arms in real-time
- DDS video streaming provides first-person view in Quest VR
- Joysticks control locomotion (forward/back/strafe/spin)
- Full arm movement (shoulders, elbows, wrists) working correctly
- macOS compatibility maintained (threading instead of multiprocessing)

**Interactive CLI Menu Complete!** Created comprehensive CLI interface for robot control. User can now:
- Switch robot modes (Debug, Motion, Damp) from terminal
- Launch teleoperation with different configurations
- Control teleoperation remotely (start with 'r', safe exit with 'q')
- Monitor status and manage full workflow from one menu

Controller mode is the recommended setup: Quest controllers for arm control, joysticks for leg locomotion.

## Recent Changes

1. **Fixed pickling error** - Modified `televuer.py` to use threading instead of multiprocessing on macOS
2. **Fixed event loop issue** - Added asyncio event loop creation in thread for Vuer server
3. **Fixed timerfd macOS issue** - Added macOS compatibility for timerfd functions
4. **DDS test script works** - Confirmed DDS connection is functional
5. **Fixed DDS initialization order** - Moved `ChannelFactoryInitialize(0, "en7")` to top level in `teleop_hand_and_arm.py` before MotionSwitcher
6. **Reduced logging frequency** - Changed from every 0.1s to once per second (fixes Ctrl+C responsiveness)
7. **Improved error handling** - Better handling of Read() errors with try/except
8. **Fixed IndexError in DDS callback** - Added empty samples list check
9. **Added DDS video streaming** - Integrated VideoClient for camera feed (no robot installation required)
10. **Added locomotion controls** - Quest joysticks control robot legs (forward/back/strafe/spin) while hand tracking controls arms
11. **Created Interactive CLI Menu** - Comprehensive control interface with mode switching, teleoperation launch, and remote control via IPC
12. **Organized documentation** - Moved all docs to `docs/` directory, updated README with CLI instructions

## Current Status

**Script Status**: ✅ **Stable and Fully Operational - Arm Control Working!**
- ✅ DDS connected successfully (connects in <1 second)
- ✅ Quest controllers controlling robot arms in real-time
- ✅ Full arm movement (shoulders, elbows, wrists) working correctly
- ✅ DDS video streaming providing first-person view in Quest VR
- ✅ Joysticks controlling locomotion (forward/back/strafe/spin)
- ✅ 'q' exit works perfectly (returns arms to home)
- ✅ Safe shutdown confirmed
- ✅ macOS threading fix applied (no pickling errors)

**Current State**: Stable arm control with visual passthrough operational
- Controller mode: Quest controllers control arms, joysticks control legs
- Hand tracking mode: Bare hands control arms, joysticks control legs
- Both modes working with locomotion enabled
- VR mode required for controllers to work (not browser mode)

## Network Configuration

- **Mac IP**: 192.168.123.56 (ethernet to switch)
- **Robot IP**: 192.168.123.164 (ethernet to switch, confirmed reachable)
- **Quest 3 IP**: 192.168.123.133 (WiFi, same network)
- **Network**: 192.168.123.X (all devices on same network)
- **Network Interface**: en7 (Mac's ethernet interface to robot)

## Status

- ✅ DDS connected and working (<1 second connection time)
- ✅ Quest controllers controlling robot arms in real-time
- ✅ Full arm movement (shoulders, elbows, wrists) working correctly
- ✅ DDS video streaming providing first-person view in Quest VR
- ✅ Joysticks controlling locomotion (forward/back/strafe/spin)
- ✅ Safe exit confirmed ('q' returns arms to home)
- ✅ VR server running (port 8012)
- ✅ Quest 3 connected and working in VR mode
- ✅ macOS threading fix applied (stable, no pickling errors)

## Next Steps

1. **Use CLI for control** - Launch `robot_control_cli.py` for interactive menu
2. **Test controller mode** - Use option 6 (Controller + Locomotion) in CLI
3. **Test full workflow** - Switch modes, launch teleop, control via CLI menu
4. **Documentation organized** - All docs in `docs/` directory, README updated

## Key Files Modified

- `dependencies/xr_teleoperate/teleop/televuer/src/televuer/televuer.py` - Fixed threading/event loop
- `dependencies/xr_teleoperate/teleop/robot_control/robot_arm.py` - Hybrid DDS approach (polling then callback), reduced logging, motion mode support
- `dependencies/xr_teleoperate/teleop/teleop_hand_and_arm.py` - **DDS initialization moved to top level** (critical fix), DDS video integration, locomotion controls added, IPC support
- `dependencies/unitree_sdk2_python/unitree_sdk2py/utils/timerfd.py` - macOS compatibility
- `dependencies/unitree_sdk2_python/unitree_sdk2py/utils/thread.py` - macOS compatibility
- `robot_control_cli.py` - **NEW**: Interactive CLI menu for complete robot control workflow
- `switch_robot_mode.py` - **NEW**: Terminal script for robot mode switching
- `README.md` - Updated with CLI instructions and documentation structure

## Important Notes

- **Port 60000 timeout is NOT a problem** - It's just camera config server, script uses local config
- **DDS initialization order matters** - Must be called at top level BEFORE MotionSwitcher (which also initializes DDS)
- **Network interface must be specified** - `en7` for Mac's ethernet connection to robot

