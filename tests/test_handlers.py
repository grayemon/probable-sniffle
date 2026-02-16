"""Unit tests for services/handlers.py"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from base.models import (
    MessageCreated,
    MessageUpdated,
    WebwidgetTriggered,
    ContactCreated,
    ContactUpdated,
    ConversationCreated,
    ConversationUpdated,
    Account,
    Contact,
    Conversation,
    Inbox,
)
from services.handlers import (
    event_handler,
    handle_message_created,
    handle_message_updated,
    handle_webwidget_triggered,
)


# Fixtures
@pytest.fixture
def mock_letta_service():
    """Mock Letta service"""
    with patch("services.handlers.letta_service") as mock:
        mock.create_conversation = AsyncMock(return_value="conv-test-123")
        mock.send_message = AsyncMock(return_value="AI response message")
        yield mock


@pytest.fixture
def mock_chatwoot_service():
    """Mock Chatwoot service"""
    with patch("services.handlers.chatwoot_service") as mock:
        mock.send_message = AsyncMock(return_value=None)
        mock.update_custom_attributes = AsyncMock(return_value=None)
        yield mock


# Test data factories
def create_message_created(
    message_type: str = "incoming",
    content: str = "Hello",
    account: Account = None,
    conversation: Conversation = None,
    custom_attributes: dict = None,
) -> MessageCreated:
    """Create a MessageCreated instance for testing"""
    conv_data = {}
    if conversation:
        conv_data = conversation.model_dump()
    elif custom_attributes is not None:
        conv_data = {"id": 1, "custom_attributes": custom_attributes}

    return MessageCreated(
        event="message_created",
        id=100,
        content=content,
        message_type=message_type,
        created_at=1234567890,
        account=account or Account(id=1, name="Test Account"),
        conversation=conv_data if conv_data else None,
    )


# Tests for event_handler routing
@pytest.mark.asyncio
async def test_event_handler_routes_message_created():
    """Test that event_handler routes message_created correctly"""
    data = create_message_created(message_type="outgoing")
    result = await event_handler(data)
    assert result["status"] == "success"
    assert result["message_id"] == 100


@pytest.mark.asyncio
async def test_event_handler_routes_message_updated():
    """Test that event_handler routes message_updated correctly"""
    data = MessageUpdated(
        event="message_updated",
        id=101,
        content="Updated content",
        message_type="incoming",
        created_at=1234567890,
        status="read",
    )
    result = await event_handler(data)
    assert result["status"] == "success"
    assert result["message_id"] == 101


@pytest.mark.asyncio
async def test_event_handler_routes_webwidget_triggered():
    """Test that event_handler routes webwidget_triggered correctly"""
    data = WebwidgetTriggered(
        event="webwidget_triggered",
        id=1,
        contact=Contact(id=1, name="Test Contact"),
        inbox=Inbox(id=1, name="Test Inbox"),
        account=Account(id=1, name="Test Account"),
        source_id="test-source-id",
        event_info={"initiated_at": "2026-01-01"},
    )
    result = await event_handler(data)
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_event_handler_routes_contact_created():
    """Test that event_handler routes contact_created correctly"""
    data = ContactCreated(
        event="contact_created",
        id=1,
        name="New Contact",
        email="test@example.com",
    )
    result = await event_handler(data)
    assert result["status"] == "success"
    assert "Contact created" in result["message"]


@pytest.mark.asyncio
async def test_event_handler_routes_contact_updated():
    """Test that event_handler routes contact_updated correctly"""
    data = ContactUpdated(
        event="contact_updated",
        id=1,
        name="Updated Contact",
    )
    result = await event_handler(data)
    assert result["status"] == "success"
    assert "Contact updated" in result["message"]


@pytest.mark.asyncio
async def test_event_handler_routes_conversation_created():
    """Test that event_handler routes conversation_created correctly"""
    data = ConversationCreated(
        event="conversation_created",
        id=1,
    )
    result = await event_handler(data)
    assert result["status"] == "success"
    assert "Conversation created" in result["message"]


@pytest.mark.asyncio
async def test_event_handler_routes_conversation_updated():
    """Test that event_handler routes conversation_updated correctly"""
    data = ConversationUpdated(
        event="conversation_updated",
        id=1,
    )
    result = await event_handler(data)
    assert result["status"] == "success"
    assert "Conversation updated" in result["message"]


# Tests for handle_message_created
@pytest.mark.asyncio
async def test_handle_message_created_outgoing_ignored(mock_letta_service, mock_chatwoot_service):
    """Test that outgoing messages are not processed"""
    data = create_message_created(message_type="outgoing")
    result = await handle_message_created(data)

    assert result["status"] == "success"
    assert result["message_id"] == 100
    # Should not call Letta or Chatwoot services
    mock_letta_service.create_conversation.assert_not_called()
    mock_letta_service.send_message.assert_not_called()
    mock_chatwoot_service.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_created_incoming_no_account(mock_letta_service, mock_chatwoot_service):
    """Test handling when account or conversation is missing"""
    data = create_message_created(
        message_type="incoming",
        account=None,
        conversation=None,
    )
    result = await handle_message_created(data)

    assert result["status"] == "success"
    assert "no account/conversation" in result["message"]
    mock_letta_service.create_conversation.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_created_with_existing_letta_conversation(
    mock_letta_service, mock_chatwoot_service
):
    """Test handling when Letta conversation already exists"""
    data = create_message_created(
        message_type="incoming",
        custom_attributes={"letta_conversation_id": "conv-existing-123"},
    )

    result = await handle_message_created(data)

    assert result["status"] == "success"
    # Should NOT create new conversation
    mock_letta_service.create_conversation.assert_not_called()
    # Should send message to existing conversation
    mock_letta_service.send_message.assert_called_once_with(
        "conv-existing-123", "Hello"
    )
    # Should send response to Chatwoot
    mock_chatwoot_service.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_handle_message_created_creates_new_letta_conversation(
    mock_letta_service, mock_chatwoot_service
):
    """Test handling when new Letta conversation needs to be created"""
    data = create_message_created(
        message_type="incoming",
        custom_attributes={},  # No existing Letta conversation
    )

    result = await handle_message_created(data)

    assert result["status"] == "success"
    # Should create new conversation
    mock_letta_service.create_conversation.assert_called_once()
    # Should update Chatwoot custom attributes
    mock_chatwoot_service.update_custom_attributes.assert_called_once()
    # Should send message to Letta
    mock_letta_service.send_message.assert_called_once()
    # Should send response to Chatwoot
    mock_chatwoot_service.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_handle_message_created_letta_creation_fails(
    mock_letta_service, mock_chatwoot_service
):
    """Test handling when Letta conversation creation fails"""
    mock_letta_service.create_conversation.return_value = None

    data = create_message_created(
        message_type="incoming",
        custom_attributes={},
    )

    result = await handle_message_created(data)

    assert result["status"] == "success"
    assert "Letta creation failed" in result["message"]
    # Should not send message or update attributes
    mock_letta_service.send_message.assert_not_called()
    mock_chatwoot_service.update_custom_attributes.assert_not_called()
    mock_chatwoot_service.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_created_letta_no_response(
    mock_letta_service, mock_chatwoot_service
):
    """Test handling when Letta returns no response"""
    mock_letta_service.send_message.return_value = None

    data = create_message_created(
        message_type="incoming",
        custom_attributes={"letta_conversation_id": "conv-test-123"},
    )

    result = await handle_message_created(data)

    assert result["status"] == "success"
    # Should not send message to Chatwoot when Letta has no response
    mock_chatwoot_service.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_created_with_conversation_object(
    mock_letta_service, mock_chatwoot_service
):
    """Test handling when conversation is a Conversation object"""
    conversation = Conversation(
        id=5,
        custom_attributes={"letta_conversation_id": "conv-obj-123"},
    )
    data = create_message_created(
        message_type="incoming",
        conversation=conversation,
    )

    result = await handle_message_created(data)

    assert result["status"] == "success"
    mock_letta_service.send_message.assert_called_once_with(
        "conv-obj-123", "Hello"
    )


# Tests for handle_message_updated
def test_handle_message_updated():
    """Test message_updated handler"""
    data = MessageUpdated(
        event="message_updated",
        id=102,
        content="Test content",
        message_type="incoming",
        created_at=1234567890,
        status="read",
    )
    result = handle_message_updated(data)

    assert result["status"] == "success"
    assert result["message_id"] == 102
    assert "Message updated" in result["message"]


# Tests for handle_webwidget_triggered
def test_handle_webwidget_triggered():
    """Test webwidget_triggered handler"""
    data = WebwidgetTriggered(
        event="webwidget_triggered",
        id=1,
        contact=Contact(id=1, name="Test Contact"),
        inbox=Inbox(id=1, name="Test Inbox"),
        account=Account(id=1, name="Test Account"),
        source_id="test-source-id",
        event_info={"initiated_at": "2026-01-01"},
        current_conversation=None,
    )
    result = handle_webwidget_triggered(data)

    assert result["status"] == "success"
    assert "Web widget triggered" in result["message"]


# Test unknown event handling via event_handler
@pytest.mark.asyncio
async def test_event_handler_unknown_event():
    """Test that unknown events are handled gracefully"""
    # Create a mock event with unknown type
    mock_event = MagicMock()
    mock_event.event = "unknown_event_type"

    result = await event_handler(mock_event)

    assert result["status"] == "success"
    assert "no handler" in result["message"]
    assert result["event"] == "unknown_event_type"
