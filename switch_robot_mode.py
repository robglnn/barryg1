#!/usr/bin/env python3
"""
Robot Mode Switcher - Switch G1 robot modes from terminal

Usage:
    python3 switch_robot_mode.py <command> [network_interface]

Commands:
    dev         - Enter Development Mode (L2+R2)
    debug       - Enter Debug Mode (L2+A, requires dev first)
    motion      - Enter Motion Mode / Regular Mode (R1+X)
    stand       - Enter Locked Standing Mode (L2+Up)
    damp        - Enter Damp Mode (soft stop, low power)
    exit_motion - Exit Motion Mode (return to Debug)
    check       - Check current robot mode

Examples:
    python3 switch_robot_mode.py dev en7
    python3 switch_robot_mode.py debug en7
    python3 switch_robot_mode.py motion en7
    python3 switch_robot_mode.py stand en7
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

def enter_dev_mode():
    """Enter Development Mode (L2+R2)"""
    try:
        print("🔄 Entering Development Mode...")
        ms = MotionSwitcher()
        # Release any current mode (enters Development Mode)
        status, result = ms.msc.CheckMode()
        if result and result.get('name'):
            print(f"   Current mode: {result.get('name')} - releasing...")
            release_status = ms.msc.ReleaseMode()
            time.sleep(1)
            print("✅ Successfully entered Development Mode")
            print("   Note: Equivalent to L2+R2 (hold both) on remote")
            print("   Next: Run 'debug' command to enter Debug Mode (L2+A)")
            return True
        else:
            print("✅ Already in Development Mode (no active mode)")
            print("   Next: Run 'debug' command to enter Debug Mode (L2+A)")
            return True
    except Exception as e:
        print(f"❌ Error entering Development Mode: {e}")
        return False

def enter_debug_mode():
    """Enter Debug Mode (L2+A, requires Dev Mode first)"""
    try:
        print("🔄 Entering Debug Mode...")
        ms = MotionSwitcher()
        # Enter Debug Mode (should be in Dev Mode first)
        status, result = ms.Enter_Debug_Mode()
        if status == 0:
            print("✅ Successfully entered Debug Mode")
            print("   Note: Equivalent to L2+A on remote")
            print("   - Use this mode for arm teleoperation without locomotion")
            return True
        else:
            print(f"⚠️  Failed to enter Debug Mode. Status: {status}")
            print("   Make sure you're in Development Mode first (run 'dev' command)")
            print("   Or manually: L2+R2 (hold both), then L2+A")
            return False
    except Exception as e:
        print(f"❌ Error entering Debug Mode: {e}")
        return False

def enter_motion_mode():
    """Enter Motion Mode - Regular Mode (R1+X)"""
    try:
        print("🔄 Entering Motion Mode (Regular Mode)...")
        ms = MotionSwitcher()
        # Enter Regular Mode (R1+X) - try "normal" first, fallback to "ai"
        print("   Entering Regular Mode (R1+X equivalent)...")
        status, result = ms.msc.SelectMode(nameOrAlias='normal')
        # Note: 3104 might be success code, check both 0 and 3104
        if status == 0 or status == 3104:
            print("✅ Successfully entered Motion Mode (Regular Mode)")
            print("   Note: Equivalent to R1+X on remote")
            print("   Use this mode for walking + arm control + streaming")
            print("   Next: Run 'stand' command for Locked Standing if needed")
            return True
        else:
            # Try "ai" as fallback
            print("   'normal' mode failed, trying 'ai' mode...")
            status, result = ms.msc.SelectMode(nameOrAlias='ai')
            if status == 0 or status == 3104:
                print("✅ Successfully entered Motion Mode (AI Mode)")
                print("   Note: Equivalent to R1+X on remote")
                print("   Use this mode for walking + arm control + streaming")
                return True
            else:
                print(f"⚠️  Failed to enter Motion Mode. Status: {status}")
                print("   Try manually: R1+X on remote")
                return False
    except Exception as e:
        print(f"❌ Error entering Motion Mode: {e}")
        return False

def locked_standing():
    """Enter Locked Standing Mode (L2+Up arrow)"""
    try:
        print("🔄 Entering Locked Standing Mode...")
        loco = LocoClientWrapper()
        # Locked standing - use Start() which puts robot in standing state
        loco.client.Start()  # FSM ID 200 = standing state
        time.sleep(1)
        # Also set balance mode for locked standing
        loco.client.BalanceStand(balance_mode=1)  # 1 = locked standing
        print("✅ Locked Standing Mode activated")
        print("   Note: Equivalent to L2+Up arrow on remote")
        print("   Use this with Motion Mode for stable standing before locomotion")
        return True
    except Exception as e:
        print(f"❌ Error entering Locked Standing: {e}")
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
    if mode == "dev":
        success = enter_dev_mode()
    elif mode == "debug":
        success = enter_debug_mode()
    elif mode == "motion" or mode == "ai":
        success = enter_motion_mode()
    elif mode == "stand":
        success = locked_standing()
    elif mode == "damp":
        success = enter_damp_mode()
    elif mode == "exit_motion":
        success = exit_motion_mode()
    elif mode == "check":
        print("✅ Mode check complete")
        sys.exit(0)
    else:
        print(f"❌ Unknown mode: {mode}")
        print("Available: dev, debug, motion, stand, damp, exit_motion, check")
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

