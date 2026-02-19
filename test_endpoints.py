#!/usr/bin/env python3
"""
Test API endpoints
"""

import requests
import time
import subprocess
import sys

def test_endpoints():
    base_url = "http://localhost:5000"
    
    # Test basic endpoint
    try:
        r = requests.get(f"{base_url}/", timeout=5)
        print(f"Home page: {r.status_code}")
    except:
        print("Server not responding")
        return
    
    # Test city suggestions
    try:
        r = requests.get(f"{base_url}/api/city_suggestions/coim", timeout=5)
        print(f"City suggestions: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Suggestions: {len(data.get('suggestions', []))}")
    except Exception as e:
        print(f"City suggestions error: {e}")
    
    # Test city data fetch
    try:
        r = requests.get(f"{base_url}/api/fetch_city_data/Coimbatore", timeout=10)
        print(f"City data fetch: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Data: {data}")
        else:
            print(f"Error response: {r.text[:100]}")
    except Exception as e:
        print(f"City data fetch error: {e}")

if __name__ == "__main__":
    test_endpoints()