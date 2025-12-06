#!/bin/bash
# XR Teleoperation Quick Start Script
cd /Users/hg/Documents/barryg1
source venv_xr_teleop_py310/bin/activate
cd dependencies/xr_teleoperate/teleop
python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive "$@"
