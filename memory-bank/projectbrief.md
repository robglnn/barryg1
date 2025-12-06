# Project Brief: Unitree G1 EDU XR Teleoperation

## Project Overview

This project sets up XR teleoperation for controlling a Unitree G1 EDU robot (23 DOF) using a Meta Quest 3 headset. The system enables real-time hand tracking and robot control through VR.

## Core Requirements

1. **Unitree SDK2** - Robot communication and control
2. **MuJoCo** - Physics simulation (for visualization/testing)
3. **Cyclone DDS** - Real-time communication middleware
4. **XR Teleoperation System** - Hand tracking and robot control via Quest 3
5. **macOS Compatibility** - All components adapted for macOS (Apple Silicon)

## Key Components

- **Robot**: Unitree G1 EDU (23 DOF)
- **XR Device**: Meta Quest 3
- **Host System**: macOS (Apple Silicon)
- **Network**: 192.168.123.X (robot, Mac, Quest 3 on same network)

## Current Status

✅ All dependencies installed and configured
✅ XR teleoperation repository cloned and set up
✅ Quest 3 connected to server
⚠️ Robot DDS connection pending (robot in debug mode, but DDS service may need configuration)

