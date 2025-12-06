# Product Requirements Document: Audio Passthrough & Hip Lean Control

## Overview

Add bidirectional audio passthrough between Quest 3 and Unitree G1 robot, and implement hip lean control using Quest right joystick.

## Feature 1: Audio Passthrough (Bidirectional)

### Requirements

1. **Quest 3 → Robot (Microphone Input)**
   - Capture audio from Quest 3 microphone
   - Stream to Unitree G1 robot speakers
   - Support stereo input (if available)
   - Low latency (<100ms end-to-end)
   - Real-time streaming (no buffering delays)

2. **Robot → Quest 3 (Speaker Output)**
   - Capture audio from Unitree G1 microphone
   - Stream to Quest 3 speakers/headphones
   - Support stereo output
   - Low latency (<100ms end-to-end)
   - Real-time streaming

### Technical Approach

**Unitree SDK Audio Capabilities:**
- `AudioClient.PlayStream(app_name, stream_id, pcm_data)` - Send PCM audio to robot speakers
- Multicast UDP (239.255.1.1:50000) - Receive audio from robot microphone
- Audio format: PCM, 16kHz, 16-bit, mono/stereo

**Quest 3 Audio:**
- Web Audio API for microphone capture
- WebRTC or WebSocket for audio streaming
- Vuer framework may support audio streaming

**Implementation Strategy:**
1. Create audio capture thread for Quest 3 mic → Robot speakers
2. Create audio capture thread for Robot mic → Quest 3 speakers
3. Use existing DDS/WebSocket infrastructure for transport
4. Handle audio format conversion (sample rate, channels, bit depth)

### User Experience

- Audio automatically streams when teleoperation is active
- No additional setup required
- Natural conversation between user and robot
- Stereo audio for immersive experience

## Feature 2: Hip Lean Control

### Requirements

- Use Quest right joystick Y-axis (forward/back) to control robot hip pitch
- Forward = lean robot forward (positive hip pitch)
- Back = lean robot backward (negative hip pitch)
- Smooth control with dead zone
- Works alongside existing locomotion controls

### Technical Approach

**Current Joystick Usage:**
- Left joystick: Forward/back (Y), Strafe left/right (X) → `vx, vy`
- Right joystick: Spin left/right (X) → `vyaw`
- **New**: Right joystick Y-axis → Hip pitch control

**Hip Control Method:**
- Use low-level DDS motor commands to control `kLeftHipPitch` and `kRightHipPitch` joints
- Joint indices: `G1_23_JointIndex.kLeftHipPitch = 0`, `kRightHipPitch = 6`
- Control via `msg.motor_cmd[joint_id].q` with appropriate `kp`, `kd` values
- Maintain current hip pitch as baseline, add offset based on joystick input

**Implementation:**
1. Extract right joystick Y-axis value: `right_thumbstickValue[1]`
2. Map to hip pitch offset (e.g., -0.3 to +0.3 radians)
3. Apply to both left and right hip pitch joints symmetrically
4. Use existing low-level DDS publisher in `robot_arm.py`

### User Experience

- Right joystick forward = robot leans forward
- Right joystick back = robot leans backward
- Smooth, proportional control
- Works in both Debug and Motion modes

## Dependencies

### Unitree SDK
- ✅ `AudioClient` - Available in `unitree_sdk2py/g1/audio/g1_audio_client.py`
- ✅ `PlayStream` API - For sending audio to robot
- ✅ Multicast UDP - For receiving audio from robot
- ✅ Low-level DDS motor control - Already used for arm control

### Quest 3 / Vuer
- ⚠️ Audio capture API - Need to verify Web Audio API support in Vuer
- ⚠️ Audio streaming - May need WebRTC or WebSocket audio extension
- ✅ Joystick input - Already implemented

## Implementation Priority

1. **High Priority**: Hip lean control (easier, uses existing infrastructure)
2. **Medium Priority**: Robot mic → Quest speakers (robot audio capture)
3. **Medium Priority**: Quest mic → Robot speakers (Quest audio capture)

## Success Criteria

- [ ] Right joystick Y-axis controls hip pitch smoothly
- [ ] Robot microphone audio streams to Quest 3 speakers
- [ ] Quest 3 microphone audio streams to robot speakers
- [ ] Stereo audio support (if hardware supports it)
- [ ] Latency < 100ms for audio passthrough
- [ ] No audio dropouts or glitches during normal operation

## Open Questions

1. Does Vuer/Quest browser support Web Audio API for microphone capture?
2. What audio format does Quest 3 microphone provide?
3. Does Unitree G1 support stereo audio, or only mono?
4. What's the optimal audio buffer size for low latency?
5. Should audio be optional (flag) or always enabled?

