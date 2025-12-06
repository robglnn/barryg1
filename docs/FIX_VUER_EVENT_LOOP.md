# Fixed Vuer Event Loop Issue

## Problem
The Vuer server was failing to start with error:
```
Vuer encountered an error: There is no current event loop in thread 'Thread-5 (_vuer_run)'.
```

This happened because when using threading instead of multiprocessing on macOS, the asyncio event loop wasn't available in the new thread.

## Solution
Modified `_vuer_run()` method to create a new event loop for the thread:

```python
def _vuer_run(self):
    try:
        # Create a new event loop for this thread (required for threading)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.vuer.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Vuer encountered an error: {e}")
    finally:
        if hasattr(self, "stop_writer_event"):
            self.stop_writer_event.set()
```

## Next Steps
1. Restart the teleoperation script
2. The Vuer server should now start properly
3. Quest 3 should be able to connect to https://192.168.123.56:8012

