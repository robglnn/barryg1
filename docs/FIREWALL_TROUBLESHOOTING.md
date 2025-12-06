# 🔥 Firewall & Network Troubleshooting

## Quick Checks

### 1. Is the Teleoperation Script Running?

The Vuer server only runs when the teleoperation script is active. Make sure you have:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh && conda activate xr_teleop && cd /Users/hg/Documents/barryg1/dependencies/xr_teleoperate/teleop && python teleop_hand_and_arm.py --arm=G1_23 --input-mode=hand --display-mode=immersive --img-server-ip=192.168.123.164
```

**The server must be running** for Quest to connect!

### 2. Check if Port 8012 is Listening

Run this on your Mac:
```bash
lsof -i :8012
```

If nothing shows up, the server isn't running or isn't listening on that port.

### 3. Mac Firewall Settings

**Option A: Temporarily Disable Firewall (for testing)**
1. System Settings → Network → Firewall
2. Turn OFF firewall temporarily
3. Try connecting from Quest
4. If it works, re-enable firewall and add exception (see Option B)

**Option B: Add Firewall Exception**
1. System Settings → Network → Firewall → Options
2. Click "+" to add application
3. Navigate to: `/opt/homebrew/Caskroom/miniconda/base/envs/xr_teleop/bin/python`
4. Allow incoming connections

**Option C: Allow Port 8012**
1. System Settings → Network → Firewall → Options
2. Click "+" to add port
3. Port: 8012
4. Protocol: TCP
5. Allow incoming connections

### 4. Test Network Connectivity

From Quest Browser, try pinging your Mac (if Quest supports it), or test from Mac:

```bash
# On Mac, test if Quest can reach you
ping 192.168.123.133
```

### 5. Check Mac's IP Address

Make sure your Mac's IP is actually 192.168.123.56:

```bash
ifconfig | grep "inet " | grep 192.168.123
```

### 6. Test from Mac Browser

Try opening `https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012` in Safari on your Mac. If it works locally but not from Quest, it's a network/firewall issue.

## Common Issues

1. **"Site can't be reached"** = Server not running OR firewall blocking
2. **"Connection refused"** = Server running but firewall blocking
3. **"Timeout"** = Network connectivity issue

## Step-by-Step Fix

1. **Start the teleoperation script** (must be running!)
2. **Check port 8012 is listening**: `lsof -i :8012`
3. **Temporarily disable Mac firewall** to test
4. **Try connecting from Quest**
5. **If it works, re-enable firewall and add exception**

