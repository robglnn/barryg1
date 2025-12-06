# ⚠️ Isaac Sim macOS Limitation

## The Problem

**Isaac Sim and Isaac Lab require:**
- Linux (Ubuntu 20.04/22.04) or Windows
- NVIDIA GPU with CUDA support (RTX 3080, 3090, 4090, or RTX 50 series)
- CUDA drivers

**macOS Limitations:**
- No NVIDIA GPU support (Apple Silicon uses Metal, not CUDA)
- Isaac Sim doesn't support macOS natively
- Docker on macOS won't have GPU acceleration

## What We Have

✅ **unitree_sim_isaaclab repository cloned** to `~/unitree_sim_isaaclab`

## Options

### Option 1: Use a Linux Machine or Cloud GPU (Recommended)

If you have access to:
- A Linux machine with NVIDIA GPU
- Cloud GPU services (AWS, Google Cloud, etc.)

You can install Isaac Sim there and run the simulation remotely.

### Option 2: Use Docker (Limited - No GPU)

You can try running in Docker, but **without GPU acceleration**, performance will be very poor:

```bash
cd ~/unitree_sim_isaaclab
sudo docker build -t unitree-sim:latest -f Dockerfile .
```

**Note**: This won't work well without GPU support.

### Option 3: Use MuJoCo Instead (Simpler Alternative)

Since you already have MuJoCo installed, you can:
1. Use MuJoCo viewer for basic visualization
2. The teleoperation script will still work, but won't have full DDS simulation

### Option 4: Connect to Physical Robot

Skip simulation entirely and connect directly to your physical G1 robot.

## Recommendation

For now, let's:
1. Keep the repository cloned (ready for when you have Linux/GPU access)
2. Use the teleoperation script with `--sim` flag - it will wait for DDS connection
3. Consider using a cloud GPU service or Linux machine for simulation

## Next Steps

Would you like me to:
1. Set up the environment files anyway (for future Linux use)?
2. Help configure MuJoCo as an alternative?
3. Focus on physical robot connection instead?

