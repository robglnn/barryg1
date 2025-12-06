# Quest Browser & DDS Fix

## Quest Browser (VR Headset)

**Quest Browser is built into your Quest 3** - you don't download it!

1. **Put on your Quest 3 headset**
2. **Open "Browser"** from the Quest home menu
3. **Navigate to**: `https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012`
   - Replace with your Mac's IP
4. **Accept SSL warning** → Click "Advanced" → "Proceed"
5. **Click "Virtual Reality"** button - This works in Quest Browser!

## DDS Test Command (Fixed for macOS)

The timerfd issue has been fixed. Try the DDS test again:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/unitree_sdk2_python/example/g1/low_level && python3 g1_low_level_example.py en7
```

This should now work on macOS!

## Current Status

- ✅ Timerfd macOS compatibility fixed
- ✅ Quest Browser info provided
- ⚠️ Still waiting for robot DDS connection

The DDS connection issue is likely because:
- Robot's PC2 DDS service may not be running
- Robot may need high-level service disabled
- Network configuration may need adjustment

