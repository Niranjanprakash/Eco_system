#!/usr/bin/env python3
"""
EcoPlan - Clean Startup Script
"""

import subprocess
import sys
import webbrowser
import time

def main():
    print("🌱 EcoPlan - AI Urban Planning Assistant")
    print("=" * 50)
    print("Starting server...")
    
    try:
        # Start Flask server
        process = subprocess.Popen([sys.executable, "app.py"])
        
        # Wait for server to start
        time.sleep(3)
        
        print("\n✅ Server started successfully!")
        print("\n📍 Available at: http://localhost:5000")
        print("\n💡 Features:")
        print("   • City autocomplete (type 'coim' for Coimbatore)")
        print("   • Automatic weather data fetching")
        print("   • Real-time location mapping")
        print("   • Sustainability analysis")
        
        # Open browser
        webbrowser.open('http://localhost:5000')
        
        print("\nPress Ctrl+C to stop...")
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        if 'process' in locals():
            process.terminate()
        print("Server stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()