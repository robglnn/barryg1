# 🤖 Physical Robot Control Setup

## Network Configuration

- **Network**: 192.168.123.X
- **Laptop (Mac)**: Connected
- **G1 Robot**: Connected (likely 192.168.123.164 or similar)
- **Quest 3**: Connected

## Step 1: Find Your Mac's IP Address

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

Note this IP address - you'll need it for Quest 3 connection.

## Step 2: Find/Confirm Robot IP Address

The robot's PC2 typically uses **192.168.123.164** (based on previous configs).

To verify, you can:
1. Check the robot's display/screen
2. Check your router's connected devices
3. Try pinging common robot IPs:
   ```bash
   ping 192.168.123.164
   ```

## Step 3: Start Teleoperation (Physical Robot)

**Single-line command:**

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --img-server-ip=192.168.123.164
```

**Replace `192.168.123.164` with your actual robot IP if different!**

## Step 4: Connect Quest 3

1. **Put on your Quest 3 headset**
2. **Open the browser** (Safari or Quest Browser)
3. **Navigate to** (replace `YOUR_MAC_IP` with your Mac's IP from Step 1):
   ```
   https://YOUR_MAC_IP:8012/?ws=wss://YOUR_MAC_IP:8012
   ```
4. **Accept the SSL certificate warning** (it's self-signed, safe to proceed)

## Step 5: Start Teleoperation

1. Wait for the script to initialize (you'll see "Waiting to subscribe dds..." until robot connects)
2. Once connected, press **'r'** in the terminal to start teleoperation
3. Your hand movements in VR will control the robot!

## Troubleshooting

### Robot Not Connecting?

1. **Check robot is powered on** and in the correct mode
2. **Verify robot IP address** is correct
3. **Check firewall** - ensure ports are open
4. **Ping the robot** to verify network connectivity:
   ```bash
   ping 192.168.123.164
   ```

### Quest 3 Can't Connect?

1. **Verify Mac and Quest 3 are on same network** (192.168.123.X)
2. **Check Mac's firewall** - allow port 8012
3. **Try using IP instead of hostname**
4. **Check Mac's IP hasn't changed**

### DDS Connection Issues?

- Make sure robot's PC2 is running and DDS is active
- Check robot is in the correct control mode
- Verify Cyclone DDS is configured on both sides

## Quick Reference Commands

### Find Mac IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

### Test Robot Connection:
```bash
ping 192.168.123.164
```

### Start Teleoperation (replace IPs as needed):
```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --img-server-ip=192.168.123.164
```

