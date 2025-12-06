# 🎮 DDS Video Test Exit & Quest Browser Testing

## How to Exit the Video Test

### Method 1: ESC Key (Recommended)
- **Press ESC** in the OpenCV window
- Script will exit cleanly
- Shows final frame count and FPS

### Method 2: Ctrl+C
- **Press Ctrl+C** in the terminal
- Will interrupt the script
- May show KeyboardInterrupt, but that's fine

## Testing DDS Video in Quest Browser

### Step 1: Run Full Teleoperation Script

**Single-line command:**

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive
```

**This will:**
- ✅ Use DDS video by default (no `--video-source` needed)
- ✅ Initialize DDS connection
- ✅ Start VideoClient for camera feed
- ✅ Start Vuer server on port 8012
- ✅ Wait for you to press 'r' to start

### Step 2: Connect Quest Browser

1. **Put on Quest 3 headset**
2. **Open Quest Browser** (built-in browser)
3. **Navigate to**: `https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012`
   - Replace `192.168.123.56` with your Mac's IP if different
4. **Click "Advanced"** → **"Proceed to IP (unsafe)"** (if security warning appears)
5. **Click "Virtual Reality" button** in the browser

### Step 3: Start Teleoperation

1. **In terminal**, wait for:
   - `DDS initialized with network interface: en7`
   - `DDS VideoClient initialized successfully`
   - `Please enter the start signal (enter 'r' to start the subsequent program)`

2. **Press 'r' in terminal** to start teleoperation

3. **In Quest VR**, you should see:
   - Robot's camera feed (from DDS video stream)
   - Your virtual hands
   - Robot arms following your movements

### Step 4: Exit Teleoperation

**Press 'q' in terminal** to safely exit:
- Robot arms return to home position
- Script exits cleanly
- DDS connection closes

## Quick Reference

### Exit Video Test
- **ESC** in OpenCV window (clean exit)
- **Ctrl+C** in terminal (interrupt)

### Run Full Teleoperation (DDS Video)
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive
```

### Quest Browser URL
```
https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012
```
(Replace with your Mac's IP)

### Controls
- **'r'** = Start teleoperation
- **'q'** = Exit safely (arms go home)

## Troubleshooting

### "VideoClient initialized successfully" but no video in Quest
- **Check**: Pressed 'r' to start?
- **Check**: Quest browser shows "Virtual Reality" button?
- **Check**: `--display-mode=immersive` (not `pass-through`)

### Video test works but Quest shows black screen
- **Wait**: Video only starts after pressing 'r'
- **Check**: Robot is in Debug Mode
- **Check**: DDS video test showed frames successfully

### Can't exit video test
- **Try**: Click on OpenCV window, then press ESC
- **Or**: Press Ctrl+C in terminal

