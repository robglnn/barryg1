#!/usr/bin/env python3
"""
Test script for DDS VideoClient
Tests video streaming from G1 robot via DDS (no teleimager required)
"""

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2
import numpy as np
import sys
import time

if __name__ == "__main__":
    # Use your network interface
    if len(sys.argv) > 1:
        network_interface = sys.argv[1]
    else:
        network_interface = "en7"
    
    print(f"Initializing DDS with network interface: {network_interface}")
    try:
        ChannelFactoryInitialize(0, network_interface)
        print("✓ DDS initialized successfully")
    except Exception as e:
        print(f"✗ DDS initialization failed: {e}")
        sys.exit(1)
    
    print("Initializing VideoClient...")
    try:
        client = VideoClient()
        client.SetTimeout(3.0)
        client.Init()
        print("✓ VideoClient initialized successfully")
    except Exception as e:
        print(f"✗ VideoClient initialization failed: {e}")
        print("Make sure robot is powered on and DDS is connected")
        sys.exit(1)
    
    print("\nStarting video stream...")
    print("Press ESC to quit")
    frame_count = 0
    start_time = time.time()
    
    while True:
        code, jpeg_data = client.GetImageSample()
        
        if code == 0:
            try:
                image_data = np.frombuffer(bytes(jpeg_data), dtype=np.uint8)
                image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
                
                if image is not None:
                    frame_count += 1
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed if elapsed > 0 else 0
                    
                    print(f"\rFrame {frame_count}: {image.shape} | FPS: {fps:.1f}", end='', flush=True)
                    
                    cv2.imshow("DDS Video Stream (G1 Robot)", image)
                    
                    if cv2.waitKey(20) == 27:  # ESC to quit
                        break
                else:
                    print("\n✗ Failed to decode JPEG image")
            except Exception as e:
                print(f"\n✗ Error processing image: {e}")
        else:
            print(f"\n✗ Error getting image: code={code}")
            print("Make sure robot is powered on and camera is working")
            break
    
    cv2.destroyAllWindows()
    print(f"\n\nTest complete. Received {frame_count} frames")
    if frame_count > 0:
        elapsed = time.time() - start_time
        avg_fps = frame_count / elapsed
        print(f"Average FPS: {avg_fps:.2f}")

