# XR Teleoperation - Current Status

## ✅ What's Working

1. All dependencies are installed:
   - Unitree SDK2 (with macOS compatibility fixes)
   - MuJoCo
   - Cyclone DDS
   - XR Teleoperation repository
   - Python environment with all required packages (pinocchio with casadi, dex-retargeting, etc.)

2. The script starts and begins initialization

## ❌ Current Issue

**Pickling Error**: `self._frozen cannot be converted to a Python object for pickling`

This occurs when `TeleVuer` tries to create a multiprocessing Process. The issue is:
- macOS uses "spawn" method for multiprocessing (default)
- "spawn" requires pickling the entire object
- The `Vuer` instance contains unpicklable objects (likely async event loops, file handles, etc.)

## Error Location

The error happens in:
- `dependencies/xr_teleoperate/teleop/televuer/src/televuer/televuer.py` line 175
- When creating: `Process(target=self._vuer_run)`

## Potential Solutions

1. **Modify the Vuer library** to create the Vuer instance inside the process (not before)
2. **Use a different multiprocessing start method** (but "fork" has issues with threading/async on macOS)
3. **Report to the library maintainers** - this is a known limitation
4. **Try using `--ipc` mode** instead of keyboard input (might avoid some issues)

## Next Steps

1. Check if there's a way to configure Vuer to avoid this issue
2. Consider if we can modify the library code locally
3. Test with a physical robot (the pickling might work in a different context)
4. Check Vuer library documentation for multiprocessing best practices

## Commands Ready

All the copy-paste commands are ready in `COPY_PASTE_COMMANDS.txt`. Once the pickling issue is resolved, the script should work.

