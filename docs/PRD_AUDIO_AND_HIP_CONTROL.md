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
- **Safety Constraint**: Only allow hip lean when locomotion is stopped (vx=0, vy=0, vyaw=0)
- **Lean Limit**: +/- 0.1 radians (~5.7 degrees) maximum
- **Transition Safety**: If user attempts locomotion while leaning, first return to normal standing (BalanceStand) before resuming movement
- Smooth control with dead zone
- Avoid jitter and conflicting motor commands

### Technical Approach

**Current Joystick Usage:**
- Left joystick: Forward/back (Y), Strafe left/right (X) → `vx, vy`
- Right joystick: Spin left/right (X) → `vyaw`
- **New**: Right joystick Y-axis → Hip pitch control (only when stationary)

**Hip Control Method:**
- Use low-level DDS motor commands to control `kLeftHipPitch` and `kRightHipPitch` joints
- Joint indices: `G1_23_JointIndex.kLeftHipPitch = 0`, `kRightHipPitch = 6`
- Control via `msg.motor_cmd[joint_id].q` with appropriate `kp`, `kd` values
- Maintain current hip pitch as baseline, add offset based on joystick input
- **Limit**: Clamp hip pitch offset to [-0.1, +0.1] radians

**State Management:**
- Track current state: `STATIONARY_LEANING` or `MOVING`
- When stationary (vx=0, vy=0, vyaw=0): Allow hip lean via right joystick Y-axis
- When moving: Disable hip lean, maintain normal standing posture
- **Transition Logic**:
  1. If leaning and user moves left joystick:
     - Set target hip pitch to 0 (neutral)
     - Wait for hip pitch to return to neutral (within tolerance)
     - Call `loco_client.BalanceStand(balance_mode=1)` to ensure stable standing
     - Small delay (e.g., 0.2s) to allow balance to stabilize
     - Then allow locomotion commands
  2. If moving and user stops (joysticks centered):
     - Wait for velocity to reach zero
     - Small delay to ensure robot is stationary
     - Then allow hip lean control

**Implementation:**
1. Extract right joystick Y-axis value: `right_thumbstickValue[1]`
2. Check if locomotion is active: `abs(vx) > 0.01 or abs(vy) > 0.01 or abs(vyaw) > 0.01`
3. If stationary:
   - Map joystick Y to hip pitch offset: `hip_pitch_offset = clamp(right_thumbstickValue[1] * 0.1, -0.1, 0.1)`
   - Apply to both left and right hip pitch joints symmetrically
4. If moving:
   - Ignore right joystick Y-axis for hip lean
   - Maintain neutral hip pitch
5. Handle transitions safely with state machine

**Safety Considerations:**
- Use dead zone for joystick input (e.g., 0.05) to prevent drift
- Smooth interpolation when transitioning between lean states
- Monitor hip pitch current position vs target to avoid sudden jumps
- Ensure BalanceStand is called before allowing movement after lean
- Add small delays between state transitions to allow robot to stabilize

### User Experience

- Right joystick forward = robot leans forward (only when stationary)
- Right joystick back = robot leans backward (only when stationary)
- Maximum lean: ~5.7 degrees forward or backward
- If user tries to move while leaning: Robot automatically returns to neutral standing, then allows movement
- Smooth, proportional control with no jitter
- Works in both Debug and Motion modes
- Hip lean disabled automatically when locomotion is active

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

### Hip Lean Control
- [ ] Right joystick Y-axis controls hip pitch smoothly (only when stationary)
- [ ] Hip lean limited to +/- 0.1 radians (~5.7 degrees)
- [ ] Hip lean automatically disabled when locomotion is active
- [ ] Safe transition: When user moves while leaning, robot returns to neutral standing before allowing movement
- [ ] No jitter or conflicting motor commands
- [ ] Smooth state transitions with appropriate delays
- [ ] BalanceStand() called before resuming locomotion after lean

### Audio Passthrough
- [ ] Robot microphone audio streams to Quest 3 speakers
- [ ] Quest 3 microphone audio streams to robot speakers
- [ ] Stereo audio support (if hardware supports it)
- [ ] Latency < 100ms for audio passthrough
- [ ] No audio dropouts or glitches during normal operation

## Open Questions

### Audio
1. Does Vuer/Quest browser support Web Audio API for microphone capture?
2. What audio format does Quest 3 microphone provide?
3. Does Unitree G1 support stereo audio, or only mono?
4. What's the optimal audio buffer size for low latency?
5. Should audio be optional (flag) or always enabled?

### Hip Lean
1. What's the optimal delay between returning to neutral and allowing locomotion? (Suggested: 0.2-0.5s)
2. What tolerance should we use to detect "neutral" hip pitch? (Suggested: 0.01 radians)
3. Should we use exponential smoothing for hip pitch changes to reduce jitter?
4. What kp/kd values should we use for hip pitch control? (May need to match existing arm control values)

