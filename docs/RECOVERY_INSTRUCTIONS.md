# Recovery Instructions: Setting Up on a New Machine

This document explains how to recover the entire project on a new machine if the current one is lost.

## ✅ What's Committed to GitHub

All critical code and fixes are committed to GitHub:

### Main Repository (`robglnn/barryg1`)
- ✅ All project files (CLI, scripts, documentation)
- ✅ Memory bank files
- ✅ README and setup instructions
- ✅ Submodule references (pointing to committed fixes)

### Submodules with macOS Fixes Committed

1. **`dependencies/xr_teleoperate`** (submodule)
   - ✅ macOS threading fix (`televuer.py`)
   - ✅ DDS initialization order fix
   - ✅ IPC file-based sockets for macOS
   - ✅ Hybrid DDS approach
   - ✅ Locomotion controls

2. **`dependencies/unitree_sdk2`** (submodule)
   - ✅ macOS header compatibility fixes
   - ✅ Scheduler constants fixes
   - ✅ Lock mechanism fixes

3. **`dependencies/unitree_sdk2_python`** (submodule)
   - ✅ timerfd macOS compatibility
   - ✅ Thread utilities for macOS
   - ✅ Channel.py fixes

## 🔄 Recovery Steps

### 1. Clone the Main Repository

```bash
git clone https://github.com/robglnn/barryg1.git
cd barryg1
```

### 2. Initialize and Update Submodules

```bash
git submodule update --init --recursive
```

This will pull all submodules with the committed fixes.

### 3. Build Dependencies

The build artifacts (symlinks, compiled files) are NOT committed (they're generated):
- `dependencies/cyclonedds/lib/arm64` - symlink (will be created during build)
- `dependencies/unitree_sdk2/lib/arm64` - symlink (will be created during build)
- Build outputs in `install/` directories

Run the build script:
```bash
./build.sh
```

### 4. Set Up Environment

Follow the README.md instructions:
- Install system dependencies via Homebrew
- Set up conda environment
- Configure environment variables

### 5. Verify Everything Works

```bash
# Test DDS connection
python3 test_dds_connection.py

# Start CLI
python3 robot_control_cli.py
```

## 📝 What's NOT Committed (and doesn't need to be)

- Build artifacts (compiled libraries, symlinks)
- Conda environment (recreated via `requirements.txt`)
- Local configuration files
- Log files

These are regenerated during setup/build process.

## ⚠️ Important Notes

1. **Submodule Commits**: The fixes are committed in the submodules' repositories. When you clone and initialize submodules, you'll get the fixed versions.

2. **Build Artifacts**: The "untracked content" warnings for `cyclonedds` and `unitree_sdk2` are just build artifacts (symlinks, compiled files). These are regenerated during the build process and don't need to be committed.

3. **Network Configuration**: You'll need to update IP addresses in scripts/CLI for your new network setup.

4. **Conda Environment**: The conda environment needs to be recreated on the new machine using the same `requirements.txt` files.

## ✅ Verification Checklist

After recovery, verify:
- [ ] All submodules initialized correctly
- [ ] Build script completes successfully
- [ ] DDS connection works
- [ ] Quest 3 can connect to Vuer server
- [ ] Robot responds to controller input
- [ ] Video streaming works in Quest VR

If any step fails, check the relevant documentation in `docs/` directory.

