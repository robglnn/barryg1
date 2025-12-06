# Product Context: XR Teleoperation System

## Purpose

Enable real-time teleoperation of Unitree G1 EDU robot using Meta Quest 3 headset for:
- Hand tracking-based robot control
- Immersive first-person view from robot's perspective
- Real-time bidirectional communication

## User Experience Goals

1. **Seamless Control**: Natural hand movements in VR control robot arms
2. **Visual Feedback**: See robot's camera feed in VR headset
3. **Low Latency**: Real-time control with minimal delay
4. **Safety**: Proper mode management and error handling

## How It Works

1. **User wears Quest 3** and sees robot's camera feed
2. **Hand tracking** captures user's hand movements
3. **Hand retargeting** converts VR hand poses to robot joint angles
4. **Inverse kinematics** calculates robot arm positions
5. **DDS communication** sends commands to robot
6. **Robot executes** movements in real-time
7. **Camera feed** streams back to VR headset

## Key Features

- **Hand Tracking**: Natural control without controllers
- **Immersive View**: First-person perspective from robot
- **Dual Arm Control**: Control both robot arms simultaneously
- **Recording**: Optional data recording for training
- **Simulation Support**: Can work with Isaac Sim (requires Linux/GPU)

## Safety Considerations

- Robot must be in correct mode (Debug Mode or Motion Mode)
- High-level motion service must be disabled to prevent conflicts
- Proper initialization sequence required
- Emergency stop capabilities

