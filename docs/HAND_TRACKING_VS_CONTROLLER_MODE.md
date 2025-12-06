# Hand Tracking vs Controller Mode - Critical Difference

## The Two Modes Are Mutually Exclusive

### 🖐️ Hand Tracking Mode (`--input-mode=hand`)
- **DO NOT hold controllers**
- Quest tracks your **bare hands** using its cameras
- Your hands must be **visible to Quest's cameras** (in front of you)
- Quest automatically switches to hand tracking when controllers are put down
- **You cannot hold controllers while using hand tracking** - Quest will switch to controller mode

### 🎮 Controller Mode (`--input-mode=controller`)
- **Hold the Quest controllers**
- Controller position/orientation controls robot arms
- Use controller joysticks for locomotion (if enabled)
- Quest is in controller mode when controllers are held

## Your Current Situation

You're running with `--input-mode=hand` but **holding controllers**. This means:
- ❌ Quest is in **controller mode** (not hand tracking)
- ❌ Hand tracking data isn't being sent to the script
- ❌ System falls back to constant poses (arms swing to default position)
- ✅ Browser XYZ interface works (manual override)

## Solution: Choose One Mode

### Option 1: Use Controller Mode (Recommended if holding controllers)
```bash
--input-mode=controller
```
- Hold controllers
- Move controllers to control robot arms
- Use joysticks for locomotion (if enabled)

### Option 2: Use Hand Tracking Mode (If you want to use bare hands)
```bash
--input-mode=hand
```
- **Put controllers down**
- Hold your hands in front of Quest cameras
- Move your hands to control robot arms
- Controllers can still be used for locomotion joysticks (if `--enable-locomotion` is set)

## Can I Hold Controllers for Hand Tracking?

**NO** - Quest automatically switches to controller mode when controllers are detected. You cannot use hand tracking while holding controllers.

## Recommended Setup

If you want to use controllers for locomotion AND hand tracking for arms:
1. Use `--input-mode=controller` for arm control
2. Use `--enable-locomotion` for joystick locomotion
3. Hold controllers and move them to control arms
4. Use joysticks to move robot legs

This is actually the **standard setup** - controller mode for arms, joysticks for locomotion.

