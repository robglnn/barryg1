# Hand Tracking Diagnosis

## Your Observations

1. **Arms swing up and to the right on startup** - This suggests the system is using **fallback constant poses** instead of real hand tracking data
2. **Only browser XYZ interface works** - This suggests hand tracking from Quest isn't being received
3. **Quest hand controllers don't control arms** - Confirms hand tracking isn't working

## What Should Happen

When `--input-mode=hand` is used:
- Quest 3 should track your **hands** (not controllers)
- Your **wrist positions** should control robot arms
- No need to hold controllers - just move your hands

## Diagnostic Steps

### 1. Check Hand Tracking in Quest Browser

The Quest browser needs to have **hand tracking enabled**. Check:
- Are you seeing your hands in the VR view?
- Is hand tracking enabled in Quest settings?
- Quest 3 requires hand tracking to be enabled in the browser session

### 2. Check Logs for Hand Tracking Status

After restarting the script, look for these log messages:
- `[Hand Tracking Debug] Left wrist pos: ...` - Shows if wrist poses are updating
- `[Hand Tracking Debug] Left wrist pose valid: ...` - Shows if using real data or fallback
- `[TeleVuer Warning] Left/Right hand tracking invalid` - Indicates hand tracking isn't working

### 3. Verify Quest Browser Connection

- Make sure Quest browser is connected to: `https://192.168.123.56:8012`
- Check that you're in **immersive mode** (not pass-through)
- Hand tracking only works in immersive VR mode

## Common Issues

### Issue 1: Hand Tracking Not Enabled in Quest
**Solution**: Quest 3 needs hand tracking enabled. Check Quest settings → Hand Tracking → Enable

### Issue 2: Browser Not Requesting Hand Tracking
**Solution**: The Vuer server needs to request hand tracking. Check that `use_hand_tracking=True` is being passed to TeleVuer

### Issue 3: Hands Not Visible in VR
**Solution**: If you don't see your hands in VR, hand tracking isn't active. Try:
- Restart Quest browser
- Reconnect to the Vuer server
- Check Quest hand tracking settings

## Browser XYZ Interface

The "red green blue XYZ" interface you mentioned is likely a **Vuer debug tool** that allows manual override of wrist poses. This is a fallback/debug feature, not the primary control method.

**If only this works**, it means:
- Hand tracking from Quest isn't reaching the script
- The system is using fallback constant poses
- Manual override via browser is the only way to control arms

## Next Steps

1. **Restart the script** with the new diagnostic logging
2. **Check the logs** for hand tracking status messages
3. **Verify Quest hand tracking** is enabled and working
4. **Report what you see** in the logs

