"""
Test script for the webhook endpoints
"""
import httpx

def test_webhook_endpoints():
    """Test all webhook endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Webhook Endpoints")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing GET /")
    response = httpx.get(f"{base_url}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 2: Health check
    print("\n2. Testing GET /health")
    response = httpx.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 3: POST webhook with JSON
    print("\n3. Testing POST /webhook (JSON)")
    test_data = {
        "event": "test",
        "data": "webhook payload",
        "timestamp": "2026-02-08T10:36:17"
    }
    response = httpx.post(f"{base_url}/webhook", json=test_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    print("\n" + "=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    test_webhook_endpoints()
