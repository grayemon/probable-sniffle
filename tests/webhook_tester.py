"""
Comprehensive webhook endpoint tests using httpx.
Tests all 7 Chatwoot event types with proper validation.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
import json
import subprocess
import time
from base.models import (
    WebhookEventAdapter,
    WebwidgetTriggered,
    MessageCreated,
)

BASE_URL = "http://127.0.0.1:8112"


class WebhookTester:
    """Test webhook endpoints with real Chatwoot event payloads"""

    def __init__(self):
        self.server_process = None

    def start_server(self):
        """Start the webhook server in background"""
        print("Starting webhook server...")
        self.server_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "tests.webhook:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8111",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        time.sleep(5)  # Wait for server to start
        print("Server started")

    def stop_server(self):
        """Stop the webhook server"""
        if self.server_process:
            print("Stopping webhook server...")
            self.server_process.terminate()
            self.server_process.wait()
            print("Server stopped")

    def test_root_endpoint(self):
        """Test GET / endpoint"""
        print("\n" + "=" * 60)
        print("Testing GET / (root endpoint)")
        print("=" * 60)

        response = httpx.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Root endpoint should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert "message" in data, "Root response should contain message"

    def test_health_endpoint(self):
        """Test GET /health endpoint"""
        print("\n" + "=" * 60)
        print("Testing GET /health (health check)")
        print("=" * 60)

        response = httpx.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Health endpoint should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "healthy", "Health status should be healthy"

    def test_contact_created(self):
        """Test POST /webhook with contact_created event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - contact_created")
        print("=" * 60)

        payload = {
            "event": "contact_created",
            "id": 6,
            "name": "morning-rain-190",
            "email": "test@example.com",
            "phone_number": "+1234567890",
            "thumbnail": "",
            "blocked": False,
            "identifier": None,
            "additional_attributes": {},
            "custom_attributes": {},
            "avatar": None,
            "account": {"id": 1, "name": "Famiglia Land Realty"},
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"

    def test_webwidget_triggered(self):
        """Test POST /webhook with webwidget_triggered event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - webwidget_triggered")
        print("=" * 60)

        payload = {
            "event": "webwidget_triggered",
            "id": 6,
            "contact": {
                "id": 6,
                "name": "morning-rain-190",
                "email": None,
                "phone_number": None,
                "thumbnail": "",
                "blocked": False,
                "type": "contact",
                "identifier": None,
                "additional_attributes": {},
                "custom_attributes": {},
                "avatar": None,
                "account": {"id": 1, "name": "Famiglia Land Realty"},
            },
            "inbox": {"id": 1, "name": "Famiglia Land Realty"},
            "account": {"id": 1, "name": "Famiglia Land Realty"},
            "current_conversation": None,
            "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
            "event_info": {
                "initiated_at": {"timestamp": "Fri Feb 13 2026 09:23:04 GMT+0800"},
                "referer": "http://localhost:3001/",
                "widget_language": "en",
                "browser_language": "en",
                "browser": {
                    "browser_name": "Microsoft Edge",
                    "browser_version": "144.0.0.0",
                    "device_name": "Unknown",
                    "platform_name": "Windows",
                    "platform_version": "10.0",
                },
            },
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"

    def test_message_created(self):
        """Test POST /webhook with message_created event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - message_created")
        print("=" * 60)

        payload = {
            "event": "message_created",
            "id": 103,
            "content": "Get notified by email",
            "message_type": 0,
            "created_at": 1770946053,
            "updated_at": "2026-02-13T01:27:33.365Z",
            "private": False,
            "status": "sent",
            "source_id": None,
            "content_type": "input_email",
            "content_attributes": {},
            "sender": None,
            "conversation": {
                "id": 6,
                "inbox_id": 1,
                "can_reply": True,
                "channel": "Channel::WebWidget",
                "contact_inbox": {
                    "id": 6,
                    "contact_id": 6,
                    "inbox_id": 1,
                    "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
                    "created_at": "2026-02-13T01:22:43.692Z",
                    "updated_at": "2026-02-13T01:22:43.692Z",
                    "hmac_verified": False,
                },
            },
            "account": {"id": 1, "name": "Famiglia Land Realty"},
            "inbox": {"id": 1, "name": "Famiglia Land Realty"},
            "additional_attributes": {},
            "content_attributes": {},
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"
        assert data["message_id"] == 103, "Should return correct message ID"

    def test_conversation_created(self):
        """Test POST /webhook with conversation_created event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - conversation_created")
        print("=" * 60)

        payload = {
            "event": "conversation_created",
            "id": 6,
            "inbox_id": 1,
            "can_reply": True,
            "channel": "Channel::WebWidget",
            "status": "open",
            "unread_count": 1,
            "priority": None,
            "labels": [],
            "custom_attributes": {},
            "additional_attributes": {
                "browser": {
                    "device_name": "Unknown",
                    "browser_name": "Microsoft Edge",
                    "platform_name": "Windows",
                    "browser_version": "144.0.0.0",
                    "platform_version": "10.0",
                },
                "referer": "http://localhost:3001/",
                "initiated_at": {"timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800"},
                "browser_language": "en",
            },
            "snoozed_until": None,
            "first_reply_created_at": None,
            "waiting_since": 1770946052,
            "agent_last_seen_at": 0,
            "contact_last_seen_at": 0,
            "last_activity_at": 1770946052,
            "timestamp": 1770946052,
            "created_at": 1770946052,
            "updated_at": 1770946052.947912,
            "contact_inbox": {
                "id": 6,
                "contact_id": 6,
                "inbox_id": 1,
                "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
                "created_at": "2026-02-13T01:22:43.692Z",
                "updated_at": "2026-02-13T01:22:43.692Z",
                "hmac_verified": False,
            },
            "meta": {
                "sender": {
                    "id": 6,
                    "name": "morning-rain-190",
                    "email": None,
                    "phone_number": None,
                    "thumbnail": "",
                    "blocked": False,
                    "type": "contact",
                    "identifier": None,
                    "additional_attributes": {},
                    "custom_attributes": {},
                    "avatar": None,
                },
                "assignee": None,
                "assignee_type": None,
                "team": None,
                "hmac_verified": False,
            },
            "messages": [],
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"

    def test_message_updated(self):
        """Test POST /webhook with message_updated event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - message_updated")
        print("=" * 60)

        payload = {
            "event": "message_updated",
            "id": 102,
            "content": "Give the team a way to reach you.",
            "message_type": "template",
            "created_at": "2026-02-13T01:27:33.358Z",
            "updated_at": "2026-02-13T01:27:33.358Z",
            "private": False,
            "status": "read",
            "source_id": None,
            "content_type": "text",
            "content_attributes": {},
            "sender": None,
            "conversation": {
                "id": 6,
                "inbox_id": 1,
                "can_reply": True,
                "channel": "Channel::WebWidget",
                "contact_inbox": {
                    "id": 6,
                    "contact_id": 6,
                    "inbox_id": 1,
                    "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
                    "created_at": "2026-02-13T01:22:43.692Z",
                    "updated_at": "2026-02-13T01:22:43.692Z",
                    "hmac_verified": False,
                },
            },
            "account": {"id": 1, "name": "Famiglia Land Realty"},
            "inbox": {"id": 1, "name": "Famiglia Land Realty"},
            "additional_attributes": {},
            "content_attributes": {},
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"
        assert data["message_id"] == 102, "Should return correct message ID"

    def test_contact_updated(self):
        """Test POST /webhook with contact_updated event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - contact_updated")
        print("=" * 60)

        payload = {
            "event": "contact_updated",
            "id": 6,
            "name": "morning-rain-190",
            "email": "updated@example.com",
            "phone_number": "+9876543210",
            "thumbnail": "",
            "blocked": False,
            "identifier": None,
            "additional_attributes": {},
            "custom_attributes": {},
            "avatar": None,
            "account": {"id": 1, "name": "Famiglia Land Realty"},
            "changed_attributes": [
                {
                    "updated_at": {
                        "previous_value": "2026-02-13T01:22:43.582Z",
                        "current_value": "2026-02-13T01:27:33.488Z",
                    }
                },
                {
                    "last_activity_at": {
                        "previous_value": None,
                        "current_value": "2026-02-13T01:27:33.485Z",
                    }
                },
            ],
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"

    def test_conversation_updated(self):
        """Test POST /webhook with conversation_updated event"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - conversation_updated")
        print("=" * 60)

        payload = {
            "event": "conversation_updated",
            "id": 6,
            "inbox_id": 1,
            "can_reply": True,
            "channel": "Channel::WebWidget",
            "status": "open",
            "unread_count": 1,
            "priority": None,
            "labels": [],
            "custom_attributes": {},
            "additional_attributes": {
                "browser": {
                    "device_name": "Unknown",
                    "browser_name": "Microsoft Edge",
                    "platform_name": "Windows",
                    "browser_version": "144.0.0.0",
                    "platform_version": "10.0",
                },
                "referer": "http://localhost:3001/",
                "initiated_at": {"timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800"},
                "browser_language": "en",
            },
            "snoozed_until": None,
            "first_reply_created_at": None,
            "waiting_since": 1770946052,
            "agent_last_seen_at": 0,
            "contact_last_seen_at": 1770946053,
            "last_activity_at": 1770946053,
            "timestamp": 1770946053,
            "created_at": 1770946052,
            "updated_at": 1770946053.629168,
            "contact_inbox": {
                "id": 6,
                "contact_id": 6,
                "inbox_id": 1,
                "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
                "created_at": "2026-02-13T01:22:43.692Z",
                "updated_at": "2026-02-13T01:22:43.692Z",
                "hmac_verified": False,
            },
            "meta": {
                "sender": {
                    "id": 6,
                    "name": "morning-rain-190",
                    "email": None,
                    "phone_number": None,
                    "thumbnail": "",
                    "blocked": False,
                    "type": "contact",
                    "identifier": None,
                    "additional_attributes": {},
                    "custom_attributes": {},
                    "avatar": None,
                },
                "assignee": None,
                "assignee_type": None,
                "team": None,
                "hmac_verified": False,
            },
            "messages": [],
            "changed_attributes": [
                {"id": {"previous_value": None, "current_value": 6}},
                {"account_id": {"previous_value": None, "current_value": 1}},
                {"inbox_id": {"previous_value": None, "current_value": 1}},
            ],
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 200, "Should return 200"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert data["status"] == "success", "Should return success status"

    def test_invalid_event(self):
        """Test POST /webhook with invalid event type"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - invalid event")
        print("=" * 60)

        payload = {"event": "invalid_event", "id": 1, "content": "test"}

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 400, "Should return 400 for invalid event"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert "error" in data["status"], "Should return error status"

    def test_missing_required_fields(self):
        """Test POST /webhook with missing required fields"""
        print("\n" + "=" * 60)
        print("Testing POST /webhook - missing required fields")
        print("=" * 60)

        payload = {
            "event": "message_created"
            # Missing required fields: id, content, message_type, created_at, content_type
        }

        print(f"Payload: {json.dumps(payload, indent=2)}")
        response = httpx.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        assert response.status_code == 400, "Should return 400 for missing fields"
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        assert "error" in data["status"], "Should return error status"

    def test_pydantic_validation(self):
        """Test Pydantic model validation directly"""
        print("\n" + "=" * 60)
        print("Testing Pydantic model validation")
        print("=" * 60)

        # Test MessageCreated validation
        message_payload = {
            "event": "message_created",
            "id": 1,
            "content": "test message",
            "message_type": 0,
            "created_at": 1234567890,
            "content_type": "text",
        }
        event = WebhookEventAdapter.validate_python(message_payload)
        print(f"Validated event type: {event.event}")
        print(f"Event class: {type(event).__name__}")
        assert isinstance(event, MessageCreated), "Should be MessageCreated instance"
        assert event.id == 1, "Should have correct id"
        assert event.content == "test message", "Should have correct content"

        # Test WebwidgetTriggered validation
        widget_payload = {
            "event": "webwidget_triggered",
            "id": 6,
            "contact": {"id": 1, "name": "test"},
            "inbox": {"id": 1, "name": "test inbox"},
            "account": {"id": 1, "name": "test account"},
            "source_id": "abc-123",
            "event_info": {"initiated_at": "2026-02-13"},
        }
        event2 = WebhookEventAdapter.validate_python(widget_payload)
        print(f"Validated event type: {event2.event}")
        print(f"Event class: {type(event2).__name__}")
        assert isinstance(
            event2, WebwidgetTriggered
        ), "Should be WebwidgetTriggered instance"

        print("[OK] Pydantic validation tests passed")

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 60)
        print("STARTING WEBHOOK TESTS")
        print("=" * 60)

        self.start_server()

        try:
            # Test endpoints
            self.test_root_endpoint()
            self.test_health_endpoint()

            # Test all 7 event types
            self.test_contact_created()
            self.test_webwidget_triggered()
            self.test_message_created()
            self.test_conversation_created()
            self.test_message_updated()
            self.test_contact_updated()
            self.test_conversation_updated()

            # Test error handling
            self.test_invalid_event()
            self.test_missing_required_fields()

            # Test Pydantic validation directly
            self.test_pydantic_validation()

            print("\n" + "=" * 60)
            print("[OK] ALL TESTS PASSED")
            print("=" * 60)

        except AssertionError as e:
            print(f"\n[FAIL] TEST FAILED: {e}")
            raise
        except Exception as e:
            print(f"\n[ERROR] {e}")
            raise
        finally:
            self.stop_server()


if __name__ == "__main__":
    tester = WebhookTester()
    tester.run_all_tests()
