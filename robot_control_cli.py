#!/usr/bin/env python3
"""
Robot Control CLI - Interactive menu for G1 robot control

Features:
- Switch robot modes (Debug, Motion, Damp)
- Launch teleoperation with different configurations
- Check robot status
- All from a single interactive menu
"""

import sys
import os
import subprocess
import time
import threading
import signal
from pathlib import Path

# Add the teleop directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dependencies', 'xr_teleoperate', 'teleop'))

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from utils.motion_switcher import MotionSwitcher, LocoClientWrapper

# IPC imports (with error handling)
try:
    from utils.ipc import IPC_Client
    IPC_AVAILABLE = True
except ImportError as e:
    IPC_AVAILABLE = False
    print(f"⚠️  IPC not available: {e}")

# Configuration
NETWORK_INTERFACE = "en7"
CONDA_ENV = "xr_teleop"
TELEOP_SCRIPT = "dependencies/xr_teleoperate/teleop/teleop_hand_and_arm.py"
ROBOT_IP = "192.168.123.164"
MAC_IP = "192.168.123.56"

class RobotControlCLI:
    def __init__(self):
        self.current_teleop_process = None
        self.running = True
        self.ipc_client = None
        self.teleop_running = False
        
    def print_header(self):
        """Print the main menu header"""
        os.system('clear' if os.name != 'nt' else 'cls')
        print("=" * 60)
        print("🤖 G1 Robot Control CLI")
        print("=" * 60)
        print()
        
    def print_menu(self):
        """Print the main menu"""
        print("📋 MAIN MENU")
        print("-" * 60)
        print()
        print("🤖 ROBOT MODES:")
        print("  [1] Enter Debug Mode      - For arm-only teleoperation")
        print("  [2] Enter Motion Mode     - For locomotion + arms")
        print("  [3] Enter Damp Mode       - Soft stop, low power")
        print("  [4] Exit Motion Mode      - Return to Debug Mode")
        print("  [5] Check Current Mode    - Show robot's current mode")
        print()
        print("🎮 TELEOPERATION:")
        print("  [6] Launch: Controller + Locomotion  - Arms (controllers) + Legs (joysticks)")
        print("  [7] Launch: Controller Only          - Arms (controllers), no locomotion")
        print("  [8] Launch: Hand Tracking + Locomotion - Arms (hands) + Legs (joysticks)")
        print("  [9] Launch: Hand Tracking Only       - Arms (hands), no locomotion")
        print()
        print("🎛️  TELEOPERATION CONTROL (when running):")
        print("  [r] Start Teleoperation              - Send 'r' to start robot following")
        print("  [q] Safe Exit                        - Send 'q' to return arms home & exit")
        print("  [s] Stop Teleoperation               - Force stop running teleoperation")
        print("  [b] Check Status                     - Show current teleoperation state")
        print()
        print("ℹ️  INFO:")
        print("  [i] Show Mode Info                   - Explain each mode")
        print("  [h] Show Help                        - Show this menu")
        print()
        print("  [x] Quit CLI                         - Exit this menu")
        print()
        print("-" * 60)
        
    def initialize_dds(self):
        """Initialize DDS connection"""
        try:
            ChannelFactoryInitialize(0, NETWORK_INTERFACE)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"❌ Error initializing DDS: {e}")
            return False
            
    def check_mode(self):
        """Check current robot mode"""
        if not self.initialize_dds():
            return None
        try:
            ms = MotionSwitcher()
            status, result = ms.msc.CheckMode()
            if status == 0 and result:
                return result.get('name', 'Unknown')
            return None
        except Exception as e:
            print(f"❌ Error checking mode: {e}")
            return None
            
    def enter_debug_mode(self):
        """Enter Debug Mode"""
        print("\n🔄 Entering Debug Mode...")
        if not self.initialize_dds():
            return False
        try:
            ms = MotionSwitcher()
            status, result = ms.Enter_Debug_Mode()
            if status == 0:
                print("✅ Successfully entered Debug Mode")
                print("   Use this mode for arm teleoperation without locomotion")
                return True
            else:
                print(f"⚠️  Failed to enter Debug Mode. Status: {status}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
            
    def enter_motion_mode(self):
        """Enter Motion Mode"""
        print("\n🔄 Entering Motion Mode (AI Mode)...")
        if not self.initialize_dds():
            return False
        try:
            ms = MotionSwitcher()
            status, result = ms.Exit_Debug_Mode()  # Exit debug = enter motion
            if status == 0:
                print("✅ Successfully entered Motion Mode")
                print("   Use this mode for locomotion + arm control")
                return True
            else:
                print(f"⚠️  Failed to enter Motion Mode. Status: {status}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
            
    def enter_damp_mode(self):
        """Enter Damp Mode"""
        print("\n🔄 Entering Damp Mode...")
        if not self.initialize_dds():
            return False
        try:
            loco = LocoClientWrapper()
            loco.Enter_Damp_Mode()
            print("✅ Successfully entered Damp Mode")
            print("   Robot is in soft stop, low power state")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
            
    def exit_motion_mode(self):
        """Exit Motion Mode (return to Debug Mode)"""
        print("\n🔄 Exiting Motion Mode (entering Debug Mode)...")
        return self.enter_debug_mode()
        
    def launch_teleop(self, input_mode, enable_locomotion, description):
        """Launch teleoperation script with IPC support"""
        if self.current_teleop_process and self.current_teleop_process.poll() is None:
            print("⚠️  Teleoperation is already running!")
            print("   Press 's' to stop it first, or wait for it to finish")
            return
            
        print(f"\n🚀 Launching teleoperation: {description}")
        print(f"   Input mode: {input_mode}")
        print(f"   Locomotion: {'Enabled' if enable_locomotion else 'Disabled'}")
        
        # Build command with --ipc flag for remote control
        conda_activate = f"source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate {CONDA_ENV}"
        
        cmd_parts = [
            "--arm=G1_23",
            f"--input-mode={input_mode}",
            "--display-mode=immersive",
            f"--img-server-ip={ROBOT_IP}",
            "--video-source=dds",
            "--ipc"  # Enable IPC for remote control
        ]
        
        if enable_locomotion:
            cmd_parts.append("--enable-locomotion")
            
        cmd = f"{conda_activate} && cd {os.path.dirname(__file__)}/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py {' '.join(cmd_parts)}"
        
        print(f"\n📝 Command: python teleop_hand_and_arm.py {' '.join(cmd_parts)}")
        print("\n⚠️  Note: Make sure robot is in the correct mode:")
        if enable_locomotion:
            print("   → Motion Mode required (press '2' to enter)")
        else:
            print("   → Debug Mode required (press '1' to enter)")
        print("\n✅ IPC mode enabled - you can control from this CLI:")
        print("   - Press 'r' in this menu to start teleoperation")
        print("   - Press 'q' in this menu to safely exit (returns arms home)")
        print("\n   Press Enter to launch, or Ctrl+C to cancel...")
        
        try:
            input()
        except KeyboardInterrupt:
            print("\n❌ Cancelled")
            return
            
        # Launch in a new terminal window (macOS)
        if sys.platform == "darwin":
            applescript = f'''
            tell application "Terminal"
                activate
                do script "{cmd}"
            end tell
            '''
            subprocess.run(['osascript', '-e', applescript])
            print("\n✅ Teleoperation launched in new terminal window")
            print("   Waiting for IPC connection...")
            
            # Initialize IPC client
            if IPC_AVAILABLE:
                time.sleep(2)  # Give teleop script time to start
                try:
                    self.ipc_client = IPC_Client(hb_fps=10.0)
                    self.teleop_running = True
                    print("✅ IPC connection established!")
                    print("   You can now use 'r' to start and 'q' to exit from this menu")
                except Exception as e:
                    print(f"⚠️  Could not connect to IPC (teleop may still be starting): {e}")
                    print("   You can still control via the teleoperation terminal")
            else:
                print("⚠️  IPC not available - you'll need to control via teleoperation terminal")
        else:
            # Fallback: run in background
            print("\n⚠️  Running in background (use 's' to stop)")
            self.current_teleop_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if IPC_AVAILABLE:
                time.sleep(2)
                try:
                    self.ipc_client = IPC_Client(hb_fps=10.0)
                    self.teleop_running = True
                except Exception as e:
                    print(f"⚠️  Could not connect to IPC: {e}")
                
    def start_teleop(self):
        """Send 'r' command to start teleoperation"""
        if not self.ipc_client:
            print("\n❌ No IPC connection. Teleoperation may not be running with --ipc flag")
            return False
        try:
            print("\n▶️  Sending start command (r)...")
            rep = self.ipc_client.send_data("CMD_START")
            if rep and rep.get('status') == 'ok':
                print("✅ Teleoperation started!")
                return True
            else:
                print(f"⚠️  Response: {rep}")
                return False
        except Exception as e:
            print(f"❌ Error sending start command: {e}")
            return False
            
    def safe_exit_teleop(self):
        """Send 'q' command to safely exit teleoperation"""
        if not self.ipc_client:
            print("\n❌ No IPC connection. Teleoperation may not be running with --ipc flag")
            print("   You can press 'q' in the teleoperation terminal instead")
            return False
        try:
            print("\n⏹️  Sending safe exit command (q)...")
            print("   This will return arms to home position before exiting")
            rep = self.ipc_client.send_data("CMD_STOP")
            if rep and rep.get('status') == 'ok':
                print("✅ Safe exit command sent!")
                print("   Robot arms will return to home position")
                return True
            else:
                print(f"⚠️  Response: {rep}")
                return False
        except Exception as e:
            print(f"❌ Error sending exit command: {e}")
            return False
            
    def check_teleop_status(self):
        """Check current teleoperation status via heartbeat"""
        if not self.ipc_client:
            print("\n❌ No IPC connection. Teleoperation may not be running with --ipc flag")
            return
        try:
            if self.ipc_client.is_online():
                state = self.ipc_client.latest_state()
                print("\n📊 Teleoperation Status:")
                print(f"   START: {state.get('START', 'Unknown')}")
                print(f"   STOP: {state.get('STOP', 'Unknown')}")
                print(f"   RECORD_RUNNING: {state.get('RECORD_RUNNING', 'Unknown')}")
                print(f"   RECORD_READY: {state.get('RECORD_READY', 'Unknown')}")
            else:
                print("\n⚠️  Teleoperation is offline (not connected)")
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            
    def stop_teleop(self):
        """Stop running teleoperation"""
        # First try safe exit via IPC
        if self.ipc_client:
            print("\n🛑 Attempting safe exit via IPC...")
            self.safe_exit_teleop()
            time.sleep(2)
            if self.ipc_client:
                self.ipc_client.stop()
                self.ipc_client = None
                self.teleop_running = False
        
        # Then kill process if still running
        if self.current_teleop_process and self.current_teleop_process.poll() is None:
            print("🛑 Force stopping teleoperation process...")
            self.current_teleop_process.terminate()
            try:
                self.current_teleop_process.wait(timeout=5)
                print("✅ Teleoperation stopped")
            except subprocess.TimeoutExpired:
                self.current_teleop_process.kill()
                print("⚠️  Force killed teleoperation")
            self.current_teleop_process = None
        else:
            print("\n⚠️  No teleoperation process running")
            
    def show_mode_info(self):
        """Show information about robot modes"""
        print("\n" + "=" * 60)
        print("📖 ROBOT MODE INFORMATION")
        print("=" * 60)
        print()
        print("🔧 DEBUG MODE:")
        print("   - Used for: Arm teleoperation without locomotion")
        print("   - Supports: Arm control via controllers/hand tracking")
        print("   - Does NOT support: Leg locomotion")
        print("   - Enter: Press '1' or use remote: L2+R2, then L2+A")
        print()
        print("🏃 MOTION MODE (AI Mode):")
        print("   - Used for: Locomotion + arm control")
        print("   - Supports: Arm control + leg locomotion simultaneously")
        print("   - Video streaming: ✅ Works")
        print("   - Arm control: ✅ Works")
        print("   - Locomotion: ✅ Works")
        print("   - Enter: Press '2' or use remote: R1+X (Regular) or R2+A (Running)")
        print()
        print("🛑 DAMP MODE:")
        print("   - Used for: Soft stop, low power state")
        print("   - Supports: No control (safe stop)")
        print("   - Enter: Press '3' or use remote: L1+R1")
        print()
        print("=" * 60)
        print("\nPress Enter to return to menu...")
        input()
        
    def show_help(self):
        """Show help information"""
        print("\n" + "=" * 60)
        print("❓ HELP")
        print("=" * 60)
        print()
        print("QUICK START:")
        print("1. Check robot mode: Press '5'")
        print("2. Enter appropriate mode:")
        print("   - For locomotion: Press '2' (Motion Mode)")
        print("   - For arms only: Press '1' (Debug Mode)")
        print("3. Launch teleoperation: Press '6', '7', '8', or '9'")
        print("4. In teleoperation terminal: Press 'r' to start")
        print()
        print("TELEOPERATION CONTROLS:")
        print("- Launch teleoperation: Options 6-9 (launches with IPC mode)")
        print("- Press 'r' in this CLI: Start teleoperation (sends 'r' command)")
        print("- Press 'q' in this CLI: Safely exit (sends 'q', returns arms home)")
        print("- Press 'b' in this CLI: Check teleoperation status")
        print("- Press 's' in this CLI: Force stop teleoperation")
        print("- Quest controllers: Move to control arms")
        print("- Quest joysticks: Control locomotion (if enabled)")
        print()
        print("NETWORK:")
        print(f"- Robot IP: {ROBOT_IP}")
        print(f"- Mac IP: {MAC_IP}")
        print(f"- Network Interface: {NETWORK_INTERFACE}")
        print()
        print("=" * 60)
        print("\nPress Enter to return to menu...")
        input()
        
    def run(self):
        """Run the CLI main loop"""
        signal.signal(signal.SIGINT, self.handle_sigint)
        
        while self.running:
            self.print_header()
            self.print_menu()
            
            # Show current mode
            current_mode = self.check_mode()
            if current_mode:
                print(f"📊 Current Robot Mode: {current_mode}")
            else:
                print("📊 Current Robot Mode: Unknown (check connection)")
            print()
            
            try:
                choice = input("Select option: ").strip().lower()
                print()
                
                if choice == '1':
                    self.enter_debug_mode()
                elif choice == '2':
                    self.enter_motion_mode()
                elif choice == '3':
                    self.enter_damp_mode()
                elif choice == '4':
                    self.exit_motion_mode()
                elif choice == '5':
                    mode = self.check_mode()
                    if mode:
                        print(f"✅ Current mode: {mode}")
                    else:
                        print("❌ Could not determine mode")
                elif choice == '6':
                    self.launch_teleop('controller', True, 
                                      'Controller + Locomotion (Arms + Legs)')
                elif choice == '7':
                    self.launch_teleop('controller', False, 
                                      'Controller Only (Arms)')
                elif choice == '8':
                    self.launch_teleop('hand', True, 
                                      'Hand Tracking + Locomotion (Arms + Legs)')
                elif choice == '9':
                    self.launch_teleop('hand', False, 
                                      'Hand Tracking Only (Arms)')
                elif choice == 'r':
                    self.start_teleop()
                elif choice == 'q':
                    if self.teleop_running or self.ipc_client:
                        print("\n⚠️  Teleoperation is running!")
                        confirm = input("   Press 'q' again to safely exit teleoperation, or any other key to cancel: ")
                        if confirm.lower() == 'q':
                            self.safe_exit_teleop()
                        else:
                            print("   Cancelled")
                    else:
                        print("\n⚠️  Teleoperation is not running")
                elif choice == 's':
                    self.stop_teleop()
                elif choice == 'b':
                    self.check_teleop_status()
                elif choice == 'i':
                    self.show_mode_info()
                elif choice == 'h':
                    self.show_help()
                elif choice == 'x':
                    print("\n👋 Quitting CLI...")
                    if self.current_teleop_process or self.ipc_client:
                        print("   Stopping teleoperation...")
                        self.stop_teleop()
                    if self.ipc_client:
                        self.ipc_client.stop()
                    self.running = False
                    break
                else:
                    print("❌ Invalid option. Press 'h' for help.")
                    
                if choice != 'q':
                    print("\nPress Enter to continue...")
                    input()
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                if self.current_teleop_process:
                    self.stop_teleop()
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
                
    def handle_sigint(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n👋 Goodbye!")
        if self.current_teleop_process:
            self.stop_teleop()
        self.running = False
        sys.exit(0)

if __name__ == "__main__":
    cli = RobotControlCLI()
    cli.run()

