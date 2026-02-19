#!/usr/bin/env python3
"""
Quick test script to verify the EcoPlan application is working correctly
"""

import requests
import time
import sys
from threading import Thread
import subprocess

def start_server():
    """Start the Flask server in a separate process"""
    try:
        subprocess.run([sys.executable, "app.py"], cwd=".", check=True)
    except Exception as e:
        print(f"Server error: {e}")

def test_endpoints():
    """Test the main endpoints"""
    base_url = "http://localhost:5000"
    
    # Wait for server to start
    time.sleep(3)
    
    endpoints_to_test = [
        "/",
        "/upload", 
        "/manual_input"
    ]
    
    print("Testing EcoPlan endpoints...")
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK (Content length: {len(response.text)} chars)")
                
                # Check if content contains expected elements
                if "EcoPlan" in response.text and len(response.text) > 1000:
                    print(f"   Content appears complete")
                else:
                    print(f"   ⚠️  Content may be incomplete")
            else:
                print(f"❌ {endpoint} - Error {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Connection error: {e}")
    
    print("\nTest completed. If all endpoints show OK with complete content, the fix is working!")

if __name__ == "__main__":
    print("Starting EcoPlan test...")
    print("This will start the server and test the main pages.")
    print("Press Ctrl+C to stop.\n")
    
    # Start server in background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test endpoints
    test_endpoints()