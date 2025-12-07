# System Patterns: XR Teleoperation Architecture

## System Architecture

```
Quest 3 (192.168.123.172)
    ↓ WebSocket/WebRTC
Mac (192.168.123.56:8012)
    ↓ DDS (Cyclone DDS)
Robot PC2 (192.168.123.164)
    ↓ Low-level control
G1 Robot Hardware
```

## Communication Patterns

### 1. XR to Mac (Vuer/WebSocket)
- **Protocol**: WebSocket (WSS) on port 8012
- **Purpose**: Hand tracking data, VR rendering
- **Library**: Vuer (runs in thread on macOS)

### 2. Mac to Robot (DDS)
- **Protocol**: DDS (Cyclone DDS) via Unitree SDK2
- **Topics**:
  - `rt/lowstate` - Robot state (subscribe)
  - `rt/lowcmd` - Robot commands (publish)
- **Purpose**: Real-time robot control
- **Initialization Pattern** (CRITICAL):
  - Must call `ChannelFactoryInitialize(0, "en7")` at **top level** before any other DDS usage
  - Must specify network interface (`en7` for Mac ethernet)
  - MotionSwitcher also initializes DDS, so must initialize before creating MotionSwitcher
  - DDS is a singleton - once initialized, can't be re-initialized
- **Connection Pattern**:
  - Use `Read()` polling to establish initial connection
  - Then switch to callback-based subscription for ongoing updates

### 3. Robot to Mac (Image Streaming)
- **Protocol**: DDS VideoClient (RPC-based) or ZMQ/WebRTC (teleimager)
- **Purpose**: Camera feed from robot to VR headset
- **DDS VideoClient**: No installation required on robot, works in Debug Mode
- **teleimager**: Alternative service (runs on robot PC2), requires installation

### 4. Audio Passthrough (Planned)
- **Quest 3 → Robot**: Web Audio API capture → AudioClient.PlayStream() → Robot speakers
- **Robot → Quest 3**: Multicast UDP (239.255.1.1:50000) → WebSocket/WebRTC → Quest speakers
- **Format**: PCM, 16kHz, 16-bit, mono/stereo
- **Latency Target**: <100ms end-to-end

### 4. Audio Passthrough (Planned)
- **Quest 3 → Robot**: Web Audio API capture → AudioClient.PlayStream() → Robot speakers
- **Robot → Quest 3**: Multicast UDP (239.255.1.1:50000) → WebSocket/WebRTC → Quest speakers
- **Format**: PCM, 16kHz, 16-bit, mono/stereo
- **Latency Target**: <100ms end-to-end

## Key Design Patterns

### Threading vs Multiprocessing
- **macOS**: Uses threading for Vuer (avoids pickling issues)
- **Linux**: Uses multiprocessing (original design)

### Error Handling
- Try/except blocks with variable existence checks
- Graceful degradation when services unavailable

### Mode Management
- **Debug Mode**: Required for teleoperation without locomotion (arms only)
- **Motion Mode**: Required for locomotion controls (legs) - use `--enable-locomotion` flag
- **MotionSwitcher**: Automatically manages mode transitions
- **Locomotion**: Uses `LocoClientWrapper` to send velocity commands (vx, vy, vyaw) to robot

### Control Modes
- **Hand Tracking Mode** (`--input-mode=hand`): Arms controlled by wrist poses from hand tracking (bare hands, no controllers)
- **Controller Mode** (`--input-mode=controller`): Arms controlled by controller positions (hold controllers, move them)
- **Locomotion** (`--enable-locomotion`): Legs controlled by Quest joysticks (works with both hand and controller modes)
  - Left joystick: Forward/back (Y-axis), Strafe left/right (X-axis)
  - Right joystick: Spin left/right (X-axis)
  - Velocity limits: 0.3 m/s linear, 0.3 rad/s angular
- **Hip Lean Control** (Planned): Right joystick Y-axis controls body pitch
  - Only active when stationary (vx=0, vy=0, vyaw=0)
  - Limited to +/- 0.1 radians (~5.7 degrees)
  - Safe transition: Returns to neutral standing before allowing locomotion
  - State machine prevents conflicting commands
- **Important**: Hand tracking and controller mode are mutually exclusive - Quest switches automatically based on whether controllers are held

## CLI Architecture

### Robot Control CLI (`robot_control_cli.py`)
- **Purpose**: Interactive menu for complete robot control workflow
- **Features**:
  - Robot mode switching (Debug, Motion, Damp)
  - Teleoperation launch with different configurations
  - Remote control via IPC (start with 'r', safe exit with 'q')
  - Status monitoring and management
- **IPC Communication**: Uses `IPC_Client` to communicate with teleoperation script when launched with `--ipc` flag
- **Mode Switching**: Uses `MotionSwitcher` and `LocoClientWrapper` for robot mode management

### Mode Switching Script (`switch_robot_mode.py`)
- **Purpose**: Standalone script for robot mode switching
- **Usage**: `python3 switch_robot_mode.py <mode> [network_interface]`
- **Modes**: debug, motion, damp, check

## Dependencies

- **Unitree SDK2**: C++ SDK for robot communication
- **unitree_sdk2_python**: Python bindings
- **Cyclone DDS**: DDS implementation
- **Vuer**: XR web framework
- **pinocchio**: Inverse kinematics (with casadi support)
- **dex-retargeting**: Hand pose retargeting
- **IPC (ZMQ)**: Inter-process communication for remote teleoperation control
- **Audio Passthrough** (Planned): Bidirectional audio streaming between Quest 3 and robot
- **Hip Lean Control** (Planned): Low-level DDS motor control for body pitch adjustment

