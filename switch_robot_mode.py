#!/usr/bin/env python3
"""
Robot Mode Switcher - Switch G1 robot modes from terminal

Usage:
    python3 switch_robot_mode.py <mode> [network_interface]

Modes:
    debug       - Enter Debug Mode (for teleoperation without locomotion)
    motion      - Enter Motion Mode / AI Mode (for locomotion)
    damp        - Enter Damp Mode (soft stop, low power)
    check       - Check current robot mode

Examples:
    python3 switch_robot_mode.py debug en7
    python3 switch_robot_mode.py motion en7
    python3 switch_robot_mode.py damp en7
    python3 switch_robot_mode.py check en7
"""

import sys
import time
import os

# Add the teleop directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dependencies', 'xr_teleoperate', 'teleop'))

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from utils.motion_switcher import MotionSwitcher, LocoClientWrapper

def check_mode():
    """Check current robot mode"""
    try:
        ms = MotionSwitcher()
        status, result = ms.msc.CheckMode()
        if status == 0 and result:
            mode_name = result.get('name', 'Unknown')
            print(f"✅ Current robot mode: {mode_name}")
            return mode_name
        else:
            print(f"⚠️  Could not check mode. Status: {status}")
            return None
    except Exception as e:
        print(f"❌ Error checking mode: {e}")
        return None

def enter_debug_mode():
    """Enter Debug Mode - for teleoperation without locomotion"""
    try:
        print("🔄 Entering Debug Mode...")
        ms = MotionSwitcher()
        status, result = ms.Enter_Debug_Mode()
        if status == 0:
            print("✅ Successfully entered Debug Mode")
            print("   - Use this mode for arm teleoperation without locomotion")
            return True
        else:
            print(f"⚠️  Failed to enter Debug Mode. Status: {status}")
            return False
    except Exception as e:
        print(f"❌ Error entering Debug Mode: {e}")
        return False

def enter_motion_mode():
    """Enter Motion Mode (AI Mode) - for locomotion"""
    try:
        print("🔄 Entering Motion Mode (AI Mode)...")
        ms = MotionSwitcher()
        status, result = ms.Exit_Debug_Mode()  # Exit debug = enter AI/motion mode
        if status == 0:
            print("✅ Successfully entered Motion Mode (AI Mode)")
            print("   - Use this mode for locomotion controls")
            return True
        else:
            print(f"⚠️  Failed to enter Motion Mode. Status: {status}")
            return False
    except Exception as e:
        print(f"❌ Error entering Motion Mode: {e}")
        return False

def enter_damp_mode():
    """Enter Damp Mode - soft stop, low power"""
    try:
        print("🔄 Entering Damp Mode...")
        loco = LocoClientWrapper()
        loco.Enter_Damp_Mode()
        print("✅ Successfully entered Damp Mode")
        print("   - Robot is in soft stop, low power state")
        return True
    except Exception as e:
        print(f"❌ Error entering Damp Mode: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    network_interface = sys.argv[2] if len(sys.argv) > 2 else "en7"
    
    # Initialize DDS with network interface
    print(f"🔌 Initializing DDS with network interface: {network_interface}")
    ChannelFactoryInitialize(0, network_interface)
    time.sleep(0.5)  # Give DDS time to initialize
    
    # Check current mode first
    print("\n📊 Checking current robot mode...")
    current_mode = check_mode()
    print()
    
    # Switch to requested mode
    success = False
    if mode == "debug":
        success = enter_debug_mode()
    elif mode == "motion" or mode == "ai":
        success = enter_motion_mode()
    elif mode == "damp":
        success = enter_damp_mode()
    elif mode == "check":
        print("✅ Mode check complete")
        sys.exit(0)
    else:
        print(f"❌ Unknown mode: {mode}")
        print(__doc__)
        sys.exit(1)
    
    if success:
        # Check mode again to confirm
        time.sleep(1)
        print("\n📊 Verifying mode change...")
        new_mode = check_mode()
        if new_mode:
            print(f"\n✅ Robot is now in: {new_mode}")
    else:
        print("\n❌ Failed to switch robot mode")
        sys.exit(1)

if __name__ == "__main__":
    main()

