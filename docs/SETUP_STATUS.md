# Installation Status

## Completed ✅

1. **Cyclone DDS** - Repository cloned
   - Location: `dependencies/cyclonedds/`
   - Status: Ready to build (requires system dependencies)

2. **Unitree SDK2** - Repository cloned
   - Location: `dependencies/unitree_sdk2/`
   - Status: Ready to build (requires Cyclone DDS and system dependencies)

3. **MuJoCo** - Python package installed
   - Version: 3.3.7 (via pip)
   - Location: `/Users/hg/Library/Python/3.9/lib/python/site-packages/mujoco/`
   - Status: ✅ Installed and ready to use

## Pending ⚠️

### System Dependencies
The following packages need to be installed via Homebrew (requires fixing Homebrew permissions first):

```bash
brew install cmake pkg-config eigen boost yaml-cpp spdlog fmt
```

**Note**: There's a Homebrew permissions issue. Fix it with:
```bash
sudo chown -R hg /opt/homebrew
```

### Build Steps Remaining

1. **Build Cyclone DDS:**
   ```bash
   cd dependencies/cyclonedds
   mkdir -p build install
   cd build
   cmake .. -DCMAKE_INSTALL_PREFIX=../install
   cmake --build . --parallel
   cmake --build . --target install
   ```

2. **Build Unitree SDK2:**
   ```bash
   cd dependencies/unitree_sdk2
   mkdir -p build
   cd build
   export CYCLONEDDS_HOME=$(pwd)/../../cyclonedds/install
   cmake ..
   cmake --build . --parallel
   sudo cmake --build . --target install
   ```

## Environment Variables

Add to `~/.zshrc`:

```bash
# Unitree G1 Development Environment
export CYCLONEDDS_HOME="$HOME/Documents/barryg1/dependencies/cyclonedds/install"
export MUJOCO_HOME="$HOME/Library/Python/3.9/lib/python/site-packages/mujoco"
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

## Next Steps

1. Fix Homebrew permissions (if needed)
2. Install system dependencies
3. Build Cyclone DDS
4. Build Unitree SDK2
5. Set environment variables
6. Test installations

