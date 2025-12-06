#!/bin/bash
# XR Teleoperation Quick Start Script (Fixed with conda)
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate xr_teleop
cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop
python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive "$@"

