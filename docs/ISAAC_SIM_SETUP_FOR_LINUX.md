# Isaac Sim Setup Instructions (For Linux/GPU Systems)

## Prerequisites

- Ubuntu 20.04 or 22.04
- NVIDIA GPU (RTX 3080, 3090, 4090, or RTX 50 series)
- CUDA drivers installed
- Conda/Miniconda installed

## Installation Steps

### Step 1: Create Conda Environment

```bash
conda create -n unitree_sim_env python=3.10  # or python=3.11 for Isaac Sim 5.0
conda activate unitree_sim_env
```

### Step 2: Install PyTorch

For CUDA 12.x:
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
```

### Step 3: Install Isaac Sim

For Isaac Sim 4.5.0:
```bash
pip install --upgrade pip
pip install 'isaacsim[all,extscache]==4.5.0' --extra-index-url https://pypi.nvidia.com
```

For Isaac Sim 5.0.0:
```bash
pip install --upgrade pip
pip install "isaacsim[all,extscache]==5.0.0" --extra-index-url https://pypi.nvidia.com
```

Verify:
```bash
isaacsim
# Accept EULA when prompted
```

### Step 4: Install Isaac Lab

```bash
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab
git checkout v2.2.0  # or specific commit for 4.5.0
sudo apt install cmake build-essential
./isaaclab.sh --install
```

Verify:
```bash
python scripts/tutorials/00_sim/create_empty.py
```

### Step 5: Install unitree_sdk2_python

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2_python
cd unitree_sdk2_python
pip3 install -e .
```

### Step 6: Install unitree_sim_isaaclab Dependencies

```bash
cd ~/unitree_sim_isaaclab
pip install -r requirements.txt
```

### Step 7: Download Assets

```bash
sudo apt install git-lfs
cd ~/unitree_sim_isaaclab
. fetch_assets.sh
```

## Running the Simulation

### For G1_23 (23 DOF):

```bash
conda activate unitree_sim_env
cd ~/unitree_sim_isaaclab
python sim_main.py --device cpu --enable_cameras --task Isaac-PickPlace-Cylinder-G123-Joint --enable_dex3_dds --robot_type g123
```

**Note**: After the window opens, click once inside it to activate!

### For G1_29 (29 DOF):

```bash
python sim_main.py --device cpu --enable_cameras --task Isaac-PickPlace-Cylinder-G129-Dex3-Joint --enable_dex3_dds --robot_type g129
```

## Current Status on macOS

❌ **Cannot run on macOS** - Requires Linux with NVIDIA GPU

✅ **Repository is ready** - Cloned to `~/unitree_sim_isaaclab`

## Alternative: Use Cloud GPU

Consider using:
- **AWS EC2** with GPU instances (g4dn, g5, etc.)
- **Google Cloud** GPU instances
- **Paperspace** or **Lambda Labs** for GPU access

