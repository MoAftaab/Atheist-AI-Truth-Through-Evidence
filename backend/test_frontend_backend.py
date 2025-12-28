"""
Test script to verify frontend-backend connection.
Run this after starting the backend server.
"""

import requests
import json

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test if backend is running."""
    print("=" * 60)
    print("Testing Backend Connection")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ Backend is running at {BACKEND_URL}")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to backend at {BACKEND_URL}")
        print("  Make sure backend is running: python run.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_api_endpoints():
    """Test key API endpoints."""
    print("\n" + "=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)
    
    # Test root
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        print(f"✓ GET / - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ GET / - Error: {e}")
    
    # Test register endpoint
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/register",
            json={"email": "test@example.com", "password": "testpass123"},
            timeout=5
        )
        status = "Created" if response.status_code == 201 else "Exists/Error"
        print(f"✓ POST /api/v1/auth/register - Status: {response.status_code} ({status})")
    except Exception as e:
        print(f"✗ POST /api/v1/auth/register - Error: {e}")
    
    # Test query endpoint
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/queries/query",
            json={"query": "What does the Quran say about fasting?", "k": 3},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ POST /api/v1/queries/query - Status: 200")
            print(f"  Answer: {data.get('answer', '')[:100]}...")
            print(f"  Citations: {len(data.get('citations', []))} verses")
        else:
            print(f"⚠ POST /api/v1/queries/query - Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print("⚠ POST /api/v1/queries/query - Timeout (this is normal for first query)")
    except Exception as e:
        print(f"✗ POST /api/v1/queries/query - Error: {e}")


def test_cors():
    """Test CORS configuration."""
    print("\n" + "=" * 60)
    print("Testing CORS Configuration")
    print("=" * 60)
    
    try:
        headers = {
            "Origin": FRONTEND_URL,
            "Access-Control-Request-Method": "POST"
        }
        response = requests.options(
            f"{BACKEND_URL}/api/v1/queries/query",
            headers=headers,
            timeout=5
        )
        
        cors_headers = {
            k: v for k, v in response.headers.items()
            if k.lower().startswith("access-control")
        }
        
        if cors_headers:
            print("✓ CORS headers present:")
            for k, v in cors_headers.items():
                print(f"  {k}: {v}")
        else:
            print("⚠ No CORS headers found")
    except Exception as e:
        print(f"✗ CORS test error: {e}")


def main():
    """Run all frontend-backend connection tests."""
    print("\n" + "=" * 60)
    print("FRONTEND-BACKEND CONNECTION TEST")
    print("=" * 60)
    
    backend_ok = test_backend_health()
    
    if backend_ok:
        test_api_endpoints()
        test_cors()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("✓ Backend is accessible")
        print("\nTo test frontend:")
        print(f"1. Start frontend: cd frontend && npm run dev")
        print(f"2. Open {FRONTEND_URL}")
        print(f"3. Check browser console for connection errors")
    else:
        print("\n✗ Backend is not running. Start it first:")
        print("  cd backend")
        print("  python run.py")


if __name__ == "__main__":
    main()


