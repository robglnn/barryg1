# 🎮 Starting Virtual Simulation with XR Teleoperation

## Overview

You need to run TWO things:
1. **The Simulation** (if using unitree_sim_isaaclab)
2. **The Teleoperation Script** (with `--sim` flag)

## Option 1: Using unitree_sim_isaaclab (Recommended)

### Step 1: Start the Simulation

First, you need to have [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) installed and set up.

**For G1_23 (23 DOF):**
```bash
# Activate your simulation environment
conda activate unitree_sim_env

# Navigate to simulation directory
cd ~/unitree_sim_isaaclab

# Start simulation for G1_23
python sim_main.py --device cpu --enable_cameras --task Isaac-PickPlace-Cylinder-G123-Joint --enable_dex3_dds --robot_type g123
```

**For G1_29 (29 DOF):**
```bash
python sim_main.py --device cpu --enable_cameras --task Isaac-PickPlace-Cylinder-G129-Dex3-Joint --enable_dex3_dds --robot_type g129
```

⚠️ **IMPORTANT**: After the simulation window opens, **click once inside the window** to activate it. You should see `controller started, start main loop...` in the terminal.

### Step 2: Start the Teleoperation Script

**In a NEW terminal window**, run:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --sim
```

### Step 3: Connect Your Quest 3

1. **Put on your Quest 3 headset**
2. **Open the browser** (Safari or Quest Browser)
3. **Navigate to** (replace `YOUR_MAC_IP` with your Mac's IP address):
   ```
   https://YOUR_MAC_IP:8012/?ws=wss://YOUR_MAC_IP:8012
   ```
4. **Accept the SSL certificate warning** (it's self-signed)

### Step 4: Start Teleoperation

Once connected:
1. The script will wait for you to press **'r'** in the terminal to start
2. Press **'r'** to begin teleoperation
3. Your hand movements in VR will control the robot in simulation!

## Option 2: Using MuJoCo Directly (Simpler, but limited)

If you don't have unitree_sim_isaaclab set up, you can use MuJoCo for basic visualization:

### Step 1: Start MuJoCo Viewer

```bash
# Install MuJoCo if not already installed
pip install mujoco

# Start MuJoCo viewer
python -m mujoco.viewer
```

### Step 2: Load the G1 Model

1. In MuJoCo viewer, drag and drop: `dependencies/xr_teleoperate/assets/g1/g1_body23.xml` (for G1_23)
2. Or use: `dependencies/xr_teleoperate/assets/g1/g1_body29_hand14.xml` (for G1_29 with hands)

### Step 3: Start Teleoperation

**In a NEW terminal**, run the teleoperation script:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --sim
```

**Note**: MuJoCo visualization is limited - it won't have full DDS communication like unitree_sim_isaaclab.

## Quick Start Commands (Copy-Paste Ready)

### Find Your Mac's IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

### Start Teleoperation (G1_23, Simulation Mode):
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --sim
```

### Quest 3 Browser URL (replace YOUR_IP):
```
https://YOUR_IP:8012/?ws=wss://YOUR_IP:8012
```

## Troubleshooting

1. **"Waiting to subscribe dds..."**: This means the simulation isn't running or DDS isn't connected. Make sure the simulation is running first.

2. **SSL Certificate Error**: This is normal. Click "Advanced" and "Proceed anyway" in your Quest 3 browser.

3. **Can't connect from Quest 3**: 
   - Make sure Quest 3 and Mac are on the same Wi-Fi network
   - Check your Mac's firewall settings
   - Verify the IP address is correct

4. **Simulation not responding**: Make sure you clicked inside the simulation window to activate it.

## Next Steps

Once everything is connected:
- Press **'r'** in the terminal to start teleoperation
- Move your hands in VR to control the robot
- Press **'s'** to stop/start recording (if using `--record` flag)
- Press **Ctrl+C** to exit

