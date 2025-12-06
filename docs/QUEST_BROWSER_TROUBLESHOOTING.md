# 🔍 Quest Browser Troubleshooting - DDS Video Mode

## Current Status from Logs

✅ **Good signs:**
- DDS initialized successfully
- DDS VideoClient initialized successfully  
- Enter debug mode: Success
- Robot controller initializing
- Script is running (waiting for DDS connection)

⚠️ **Issues:**
- No explicit "Vuer server started" message in logs
- Quest browser not loading the VR interface
- Script waiting for DDS connection (may be blocking Vuer startup)

## What Should Happen

1. **TeleVuerWrapper initializes** → Starts Vuer server in background thread
2. **Vuer server listens** → Port 8012 (HTTPS)
3. **Script continues** → Waits for DDS connection, then waits for 'r'
4. **Quest browser connects** → Shows VR interface

## Troubleshooting Steps

### Step 1: Check if Vuer Server is Running

**In a new terminal, check if port 8012 is listening:**

```bash
lsof -i :8012
```

**Or check with netstat:**

```bash
netstat -an | grep 8012
```

**Expected:** Should show Python process listening on port 8012

### Step 2: Verify Quest Browser URL

**Correct URL format:**
```
https://192.168.123.56:8012/?ws=wss://192.168.123.56:8012
```

**Replace `192.168.123.56` with your Mac's actual IP:**
- Check with: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- Or: `ipconfig getifaddr en7` (for your ethernet interface)

### Step 3: Check SSL Certificates

Vuer requires SSL certificates. Check if they exist:

```bash
ls -la ~/.config/xr_teleoperate/cert.pem ~/.config/xr_teleoperate/key.pem
```

**Or check in televuer directory:**
```bash
ls -la dependencies/xr_teleoperate/teleop/televuer/cert.pem dependencies/xr_teleoperate/teleop/televuer/key.pem
```

### Step 4: Wait for Script to Fully Initialize

The script might still be initializing. **Wait for this message:**
```
Please enter the start signal (enter 'r' to start the subsequent program)
```

**Only then** should you try connecting with Quest browser.

### Step 5: Check Quest Browser

1. **Open Quest Browser** (not regular browser)
2. **Navigate to**: `https://YOUR_MAC_IP:8012/?ws=wss://YOUR_MAC_IP:8012`
3. **Click "Advanced"** → **"Proceed to IP (unsafe)"** if security warning
4. **Look for**: "Virtual Reality" button or VR interface

## Common Issues

### Issue 1: Port 8012 Not Listening

**Symptom**: `lsof -i :8012` shows nothing

**Possible causes:**
- Vuer server thread hasn't started yet
- Script crashed before Vuer started
- SSL certificate issue preventing server start

**Solution**: Wait a few seconds, check again. If still nothing, check for errors in logs.

### Issue 2: "Site Can't Be Reached"

**Symptom**: Quest browser shows connection error

**Possible causes:**
- Wrong IP address
- Firewall blocking port 8012
- Vuer server not started
- Network issue

**Solution**: 
- Verify Mac IP: `ifconfig | grep "inet "`
- Check firewall: System Settings → Network → Firewall
- Verify port is listening: `lsof -i :8012`

### Issue 3: Security Warning in Quest Browser

**Symptom**: "Your connection is not private" warning

**This is normal!** Vuer uses self-signed certificates.

**Solution**: Click "Advanced" → "Proceed to IP (unsafe)"

### Issue 4: No "Virtual Reality" Button

**Symptom**: Page loads but no VR button

**Possible causes:**
- Page not fully loaded
- JavaScript error
- Wrong URL format

**Solution**: 
- Wait a few seconds for page to load
- Check browser console for errors
- Verify URL format is correct

## Quick Diagnostic Commands

### Check Mac IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Check if port 8012 is listening:
```bash
lsof -i :8012
```

### Check SSL certificates:
```bash
ls -la ~/.config/xr_teleoperate/cert.pem ~/.config/xr_teleoperate/key.pem
```

### Test HTTPS connection from Mac:
```bash
curl -k https://localhost:8012
```

## Expected Log Sequence

When everything works, you should see:

1. `Using DDS video source (no teleimager required)`
2. `DDS initialized with network interface: en7`
3. `DDS VideoClient initialized successfully`
4. `Enter debug mode: Success`
5. `[G1_23_ArmController] Initializing DDS subscriber...`
6. `[G1_23_ArmController] DDS connection established!`
7. `[G1_23_ArmController] Subscribe dds ok.`
8. `Please enter the start signal (enter 'r' to start...)`

**At this point**, Vuer server should be running and Quest browser should connect.

## Next Steps

1. **Check if port 8012 is listening** (use command above)
2. **Verify your Mac's IP address**
3. **Try Quest browser URL** with correct IP
4. **Wait for "Please enter the start signal"** message before connecting
5. **Check for any error messages** in the logs

