#!/usr/bin/env python3
"""
Test script for UDP Video6 client
Tests receiving video6 stream from G1 robot server at 1920x1080
"""

import sys
import os

# Add teleop directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
teleop_dir = os.path.join(current_dir, "dependencies", "xr_teleoperate", "teleop")
sys.path.insert(0, teleop_dir)

from udp_video_client import UDPVideoClient
import cv2
import time
import logging_mp

# Enable debug logging to see what's happening
logging_mp.basic_config(level=logging_mp.INFO)

if __name__ == "__main__":
    # Default to video6 from robot on port 5002
    robot_ip = sys.argv[1] if len(sys.argv) > 1 else "192.168.123.164"
    
    print(f"Testing UDP VideoClient: video6 from {robot_ip}")
    print(f"Expected resolution: 1920x1080")
    print(f"Listening on port: 5002")
    
    client = UDPVideoClient(
        robot_ip=robot_ip,
        port=5002,
        width=1920,
        height=1080,
        max_fps=24.0  # Limit to 24 FPS for consistent playback
    )
    
    if not client.start():
        print("✗ Failed to start UDP video client")
        print("Make sure:")
        print("  1. Robot UDP video server is running")
        print("  2. Robot is broadcasting video6 stream")
        print("  3. Network connection to robot is working")
        sys.exit(1)
    
    print("✓ UDP VideoClient started")
    print("Receiving video stream... Press ESC to quit")
    print("Note: Check terminal for [UDP] log messages showing packet reception and decoding")
    print("Waiting for frames...")
    
    frame_count = 0
    start_time = time.time()
    no_frame_count = 0
    
    try:
        last_frame_time = 0
        while True:
            frame = client.get_frame()
            if frame is not None:
                frame_count += 1
                current_time = time.time()
                
                # Calculate actual output FPS (not decode FPS)
                if last_frame_time > 0:
                    elapsed = current_time - last_frame_time
                    output_fps = 1.0 / elapsed if elapsed > 0 else 0
                else:
                    output_fps = 0
                last_frame_time = current_time
                
                elapsed_total = time.time() - start_time
                avg_fps = frame_count / elapsed_total if elapsed_total > 0 else 0
                
                # Print status
                status = f"\r✓ Frame {frame_count}: {frame.shape} | Output FPS: {output_fps:.1f} | Avg FPS: {avg_fps:.1f}"
                print(status, end='', flush=True)
                
                # Display frame
                cv2.imshow(f"UDP Video Stream - video6 ({frame.shape[1]}x{frame.shape[0]})", frame)
                
                if cv2.waitKey(1) == 27:  # ESC
                    break
                no_frame_count = 0  # Reset counter when we get frames
            else:
                no_frame_count += 1
                if no_frame_count == 1:
                    print("\n[INFO] Waiting for first frame... (packets may be arriving but not decoded yet)")
                elif no_frame_count % 500 == 0:  # Print every ~5 seconds
                    print(f"\r[INFO] Still waiting... ({no_frame_count * 0.01:.1f}s elapsed, {client.get_frame_count()} frames decoded)", end='', flush=True)
                # Small delay to prevent tight loop when throttled
                time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        client.stop()
        cv2.destroyAllWindows()
        elapsed = time.time() - start_time
        print(f"\n\nTest complete!")
        print(f"  Total frames received: {frame_count}")
        if frame_count > 0:
            print(f"  Average FPS: {frame_count / elapsed:.2f}")
            print(f"  Total time: {elapsed:.1f} seconds")

