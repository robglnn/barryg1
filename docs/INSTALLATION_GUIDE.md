# Unitree G1 EDU Installation Guide

## Summary

I've successfully located and cloned the required repositories for your Unitree G1 EDU (23 DOF) development environment:

✅ **Cyclone DDS** - Cloned from GitHub  
✅ **Unitree SDK2** - Cloned from GitHub  
✅ **MuJoCo** - Installed via pip (Python package)

## Current Status

### Installed Components

1. **Cyclone DDS** (`dependencies/cyclonedds/`)
   - Repository: https://github.com/eclipse-cyclonedds/cyclonedds
   - Branch: releases/0.10.x
   - Status: Cloned, ready to build

2. **Unitree SDK2** (`dependencies/unitree_sdk2/`)
   - Repository: https://github.com/unitreerobotics/unitree_sdk2
   - Status: Cloned, ready to build

3. **MuJoCo** (Python package)
   - Version: 3.3.7
   - Installed via: `pip3 install mujoco`
   - Location: `/Users/hg/Library/Python/3.9/lib/python/site-packages/mujoco/`
   - Status: ✅ Installed and ready to use

### Required System Dependencies

Before building, you need to install these via Homebrew:

```bash
brew install cmake pkg-config eigen boost yaml-cpp spdlog fmt
```

**Important**: There's a Homebrew permissions issue that needs to be fixed first:

```bash
sudo chown -R hg /opt/homebrew
```

## Installation Steps

### Step 1: Fix Homebrew Permissions (if needed)

```bash
sudo chown -R hg /opt/homebrew
```

### Step 2: Install System Dependencies

```bash
brew install cmake pkg-config eigen boost yaml-cpp spdlog fmt
```

### Step 3: Build Cyclone DDS

```bash
cd dependencies/cyclonedds
mkdir -p build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel
cmake --build . --target install
```

This installs Cyclone DDS to `dependencies/cyclonedds/install/`

### Step 4: Build Unitree SDK2

```bash
cd dependencies/unitree_sdk2
mkdir -p build
cd build
export CYCLONEDDS_HOME=$(pwd)/../../cyclonedds/install
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel
sudo cmake --build . --target install
```

### Step 5: Set Environment Variables

Add to your `~/.zshrc`:

```bash
# Unitree G1 Development Environment
export CYCLONEDDS_HOME="$HOME/Documents/barryg1/dependencies/cyclonedds/install"
export MUJOCO_HOME="$(python3 -c 'import mujoco; import os; print(os.path.dirname(mujoco.__file__))')"
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
export DYLD_LIBRARY_PATH="$MUJOCO_HOME/bin:$DYLD_LIBRARY_PATH"
```

Then reload:

```bash
source ~/.zshrc
```

## Quick Build Script

After fixing Homebrew permissions and installing dependencies, you can use the build script:

```bash
./build.sh
```

## Verification

### Test MuJoCo

```python
python3 -c "import mujoco; print('MuJoCo version:', mujoco.__version__)"
```

### Test Cyclone DDS

```bash
cd dependencies/cyclonedds
# Check if binaries are built
ls install/bin/
```

### Test Unitree SDK2

```bash
cd dependencies/unitree_sdk2
# Check examples directory
ls examples/
```

## Project Structure

```
barryg1/
├── dependencies/
│   ├── cyclonedds/          # Cyclone DDS source and build
│   │   ├── build/           # Build directory
│   │   └── install/         # Installation directory
│   ├── mujoco/              # (MuJoCo installed via pip)
│   └── unitree_sdk2/        # Unitree SDK2 source
│       └── build/           # Build directory
├── build.sh                 # Build script
├── install.sh               # Full installation script
├── README.md                # Project documentation
├── SETUP_STATUS.md          # Current status
└── INSTALLATION_GUIDE.md    # This file
```

## Troubleshooting

### Homebrew Permission Issues

If you see permission errors with Homebrew:
```bash
sudo chown -R $(whoami) /opt/homebrew
```

### CMake Not Found

Install CMake:
```bash
brew install cmake
```

### Build Errors

1. Ensure all dependencies are installed
2. Check that `CYCLONEDDS_HOME` is set before building Unitree SDK2
3. Verify Xcode Command Line Tools: `xcode-select --install`

### MuJoCo Import Errors

If Python can't find MuJoCo:
```bash
pip3 install --upgrade mujoco
python3 -c "import mujoco; print(mujoco.__file__)"
```

## Next Steps

1. Fix Homebrew permissions
2. Install system dependencies
3. Run `./build.sh` or follow manual build steps
4. Set environment variables
5. Start developing control algorithms for your Unitree G1 EDU!

## Resources

- [Unitree SDK2 GitHub](https://github.com/unitreerobotics/unitree_sdk2)
- [Cyclone DDS Documentation](https://cyclonedds.io/)
- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [Unitree G1 Documentation](https://www.unitree.com/products/g1)

