# Technical Context

## Technologies

### Core Stack
- **Python 3.10** (via conda)
- **Unitree SDK2** (C++ with Python bindings)
- **Cyclone DDS 0.10.x** (DDS middleware)
- **MuJoCo 3.3.7** (physics simulation)
- **Vuer** (XR web framework)

### Python Packages
- **pinocchio** (3.1.0 with casadi support) - via conda
- **dex-retargeting** (0.4.7) - hand retargeting
- **torch** (2.3.0) - deep learning
- **numpy** (<2.0.0) - numerical computing
- **nlopt** (2.10.0) - optimization (via conda)

### Platform
- **OS**: macOS (darwin 25.0.0)
- **Architecture**: Apple Silicon (arm64)
- **Shell**: zsh

## Development Setup

### Environments
- **Conda**: `xr_teleop` (Python 3.10)
- **Location**: `/opt/homebrew/Caskroom/miniconda/base/envs/xr_teleop`

### Key Directories
- **Project Root**: `/Users/hg/Documents/barryg1`
- **Dependencies**: `dependencies/`
- **XR Teleoperation**: `dependencies/xr_teleoperate/`
- **Unitree SDK2**: `dependencies/unitree_sdk2/`
- **Cyclone DDS**: `dependencies/cyclonedds/`

## macOS Compatibility Fixes

### Unitree SDK2
1. **Linux headers**: Conditionally removed `sys/sysinfo.h`, `sys/timerfd.h`
2. **Spinlock**: Replaced `pthread_spinlock_t` with `os_unfair_lock`
3. **Scheduler**: Removed Linux-specific scheduler constants
4. **Library path**: Created symlink `lib/arm64` → `lib/aarch64`

### TeleVuer
1. **Multiprocessing**: Switched to threading on macOS (avoids pickling)
2. **Event loop**: Added asyncio event loop creation in thread

### Unitree SDK2 Python
1. **Timerfd**: Added macOS compatibility (uses time.sleep fallback)
2. **DDS Subscription**: Converting from polling (`Read()`) to callback-based (`Init(handler, queueLen)`)

## Network Configuration

- **Protocol**: DDS over UDP (Cyclone DDS)
- **Ports**: 
  - 8012 (Vuer/WebSocket)
  - 60000 (teleimager config)
  - 60001 (WebRTC)
  - DDS uses dynamic ports

## Build System

- **CMake**: For C++ components (Unitree SDK2, Cyclone DDS)
- **pip/conda**: For Python packages
- **Homebrew**: System dependencies

