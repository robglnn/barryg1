# UDP Video Client for G1 Robot

## Overview

This UDP video client receives video streams from the G1 robot's UDP video server. The server broadcasts video streams for video2, video4, and video6 on different UDP ports.

Based on the architecture from: https://github.com/xvanov/unitree-g1-robot/tree/simple-arch

## Architecture

```
Robot PC2 (192.168.123.164)
    ↓ UDP Broadcast
    video2, video4, video6 streams
    ↓ Network (UDP)
Your Mac (192.168.123.56)
    ↓ UDP VideoClient
    Video frames (1920x1080)
    ↓ TeleVuer
Quest 3 VR Headset
```

## Port Configuration

The UDP video server uses the following port scheme:
- **video2**: Port 50002 (50000 + 2)
- **video4**: Port 50004 (50000 + 4)
- **video6**: Port 50006 (50000 + 6)

Each video source broadcasts JPEG-encoded frames via UDP.

## Usage

### Test UDP Video Client

Test the UDP video client standalone:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate xr_teleop
cd /Users/hg/Documents/barryg1
python test_udp_video6.py [robot_ip] [video_source]
```

Examples:
```bash
# Test video6 from default robot IP
python test_udp_video6.py

# Test video6 from specific robot IP
python test_udp_video6.py 192.168.123.164 video6

# Test video4
python test_udp_video6.py 192.168.123.164 video4
```

### Use in Teleoperation

Run teleoperation with UDP video source:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate xr_teleop
cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop
python teleop_hand_and_arm.py --arm=G1_23 --input-mode=controller \
  --display-mode=immersive \
  --img-server-ip=192.168.123.164 --enable-locomotion
```

### Command-Line Arguments

- `--video-source=udp`: Use UDP video source (now the default, can be omitted)
- Note: Currently hardcoded to video6 on port 5002 (1920x1080 resolution)
- `--img-server-ip=192.168.123.164`: Robot IP address (used for UDP connection)

## Video Source Selection

The UDP video client supports receiving from:
- **video2**: Typically a side or auxiliary camera
- **video4**: Another camera source
- **video6**: Forward-facing USB camera for VR headset (1920x1080)

## Implementation Details

### UDPVideoClient Class

Located in: `dependencies/xr_teleoperate/teleop/udp_video_client.py`

**Key Features:**
- Receives JPEG-encoded frames via UDP
- Automatically decodes frames using OpenCV
- Resizes frames to expected resolution (1920x1080)
- Thread-safe frame retrieval
- FPS calculation and monitoring

**Methods:**
- `start()`: Start receiving video stream in background thread
- `stop()`: Stop receiving and close socket
- `get_frame()`: Get latest frame (BGR format, numpy array)
- `get_fps()`: Get current FPS of received stream
- `get_frame_count()`: Get total number of frames received

### Integration with Teleoperation

The UDP video client is integrated into `teleop_hand_and_arm.py`:
1. Initialized when `--video-source=udp` is specified
2. Receives frames in background thread
3. Frames are retrieved in main loop and sent to Quest VR headset
4. Automatically cleaned up on exit

## Troubleshooting

### No Frames Received

1. **Check robot server is running:**
   - Verify UDP video server is broadcasting on robot
   - Check that video6 stream is active

2. **Check network connection:**
   ```bash
   ping 192.168.123.164
   ```

3. **Check port is accessible:**
   ```bash
   # On Mac, check if port is listening (should show UDP packets)
   netstat -an | grep 50006
   ```

4. **Check firewall:**
   - Ensure UDP ports 50002, 50004, 50006 are not blocked
   - macOS firewall may need to allow Python network access

### Wrong Resolution

- The client automatically resizes frames to 1920x1080
- If frames are a different size, they will be resized
- Check logs for actual frame dimensions received

### Low FPS

- UDP video streaming depends on network conditions
- Check network latency: `ping 192.168.123.164`
- Ensure robot and Mac are on same network segment
- Check for network congestion

## Comparison with Other Video Sources

| Feature | DDS VideoClient | Teleimager | UDP VideoClient |
|---------|----------------|------------|-----------------|
| Video Source Selection | ❌ No (uses videohub default) | ✅ Yes (via config) | ✅ Yes (video2/4/6) |
| Resolution | 1920x1080 | Configurable | 1920x1080 (video6) |
| Protocol | DDS RPC | ZMQ/WebRTC | UDP |
| Robot Install Required | ❌ No | ✅ Yes | ❌ No (server runs on robot) |
| Latency | Medium | Low | Low |
| Setup Complexity | Low | Medium | Low |

## Next Steps

1. **Test video6 stream:**
   ```bash
   python test_udp_video6.py
   ```

2. **Verify 1920x1080 resolution:**
   - Check frame dimensions in test output
   - Verify image quality in Quest VR headset

3. **Use in teleoperation:**
   - Run with `--video-source=udp --udp-video-source=video6`
   - Verify video appears correctly in Quest VR

## Notes

- The UDP video server must be running on the robot before starting the client
- Video6 is specifically configured for forward views in VR headset
- Frames are received asynchronously in a background thread for low latency
- The client handles fragmented UDP packets and various header formats automatically

