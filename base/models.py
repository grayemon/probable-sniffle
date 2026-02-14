from pydantic import BaseModel, Field
from pydantic import TypeAdapter
from typing import Optional, Dict, List, Any, Union, Literal, Annotated


class Account(BaseModel):
    id: int
    name: str


class Contact(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    thumbnail: str = ""
    blocked: bool = False
    type: str = "contact"
    identifier: Optional[str] = None
    additional_attributes: Dict[str, Any] = {}
    custom_attributes: Dict[str, Any] = {}
    avatar: Optional[str] = None
    account: Optional[Account] = None


class ContactInbox(BaseModel):
    id: int
    contact_id: int
    inbox_id: int
    source_id: str
    created_at: str
    updated_at: str
    hmac_verified: bool = False
    pubsub_token: Optional[str] = None


class Conversation(BaseModel):
    id: int
    inbox_id: Optional[int] = None
    can_reply: Optional[bool] = None
    channel: Optional[str] = None
    status: Optional[str] = None
    unread_count: Optional[int] = None
    priority: Optional[str] = None
    labels: List[str] = []
    custom_attributes: Dict[str, Any] = {}
    additional_attributes: Dict[str, Any] = {}
    snoozed_until: Optional[Any] = None
    first_reply_created_at: Optional[Any] = None
    waiting_since: Optional[int] = None
    agent_last_seen_at: Optional[int] = None
    contact_last_seen_at: Optional[int] = None
    last_activity_at: Optional[int] = None
    timestamp: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[float] = None
    contact_inbox: Optional[ContactInbox] = None
    meta: Optional[Dict[str, Any]] = None
    messages: Optional[List[Dict[str, Any]]] = None


class Inbox(BaseModel):
    id: int
    name: str


class Message(BaseModel):
    id: int
    content: str
    message_type: Union[int, str] = 0
    created_at: Union[int, str]
    updated_at: Optional[Union[int, str]] = None
    private: bool = False
    status: Optional[str] = None
    source_id: Optional[str] = None
    content_type: str = "text"
    content_attributes: Dict[str, Any] = {}
    sender_type: Optional[str] = None
    sender_id: Optional[int] = None
    external_source_ids: Dict[str, Any] = {}
    additional_attributes: Dict[str, Any] = {}
    processed_message_content: Optional[str] = None
    sentiment: Dict[str, Any] = {}
    account_id: Optional[int] = None
    inbox_id: Optional[int] = None
    conversation_id: Optional[int] = None
    conversation: Optional[Dict[str, Any]] = None
    sender: Optional[Contact] = None


class Sender(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    thumbnail: str = ""
    blocked: bool = False
    type: str = "contact"
    identifier: Optional[str] = None
    additional_attributes: Dict[str, Any] = {}
    custom_attributes: Dict[str, Any] = {}
    avatar: Optional[str] = None
    account: Optional[Account] = None


# Event-specific models using discriminated unions
class ContactCreated(BaseModel):
    event: Literal["contact_created"]
    id: int
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    thumbnail: str = ""
    blocked: bool = False
    identifier: Optional[str] = None
    additional_attributes: Dict[str, Any] = {}
    custom_attributes: Dict[str, Any] = {}
    avatar: Optional[str] = None
    account: Optional[Account] = None


class WebwidgetTriggered(BaseModel):
    event: Literal["webwidget_triggered"]
    id: int
    contact: Contact
    inbox: Inbox
    account: Account
    current_conversation: Optional[Any] = None
    source_id: str
    event_info: Dict[str, Any]


class MessageCreated(BaseModel):
    event: Literal["message_created"]
    id: int
    content: str
    message_type: Union[int, str]
    created_at: Union[int, str]
    updated_at: Optional[Union[int, str]] = None
    private: bool = False
    status: Optional[str] = None
    source_id: Optional[str] = None
    content_type: str = "text"
    content_attributes: Dict[str, Any] = {}
    sender: Optional[Union[Contact, Dict[str, Any]]] = None
    conversation: Optional[Union[Conversation, Dict[str, Any]]] = None
    account: Optional[Account] = None
    inbox: Optional[Inbox] = None
    additional_attributes: Dict[str, Any] = {}
    content_attributes: Optional[Dict[str, Any]] = None


class ConversationCreated(BaseModel):
    event: Literal["conversation_created"]
    id: int
    inbox_id: Optional[int] = None
    can_reply: Optional[bool] = None
    channel: Optional[str] = None
    status: Optional[str] = None
    unread_count: Optional[int] = None
    priority: Optional[str] = None
    labels: List[str] = []
    custom_attributes: Dict[str, Any] = {}
    additional_attributes: Dict[str, Any] = {}
    snoozed_until: Optional[Any] = None
    first_reply_created_at: Optional[Any] = None
    waiting_since: Optional[int] = None
    agent_last_seen_at: Optional[int] = None
    contact_last_seen_at: Optional[int] = None
    last_activity_at: Optional[int] = None
    timestamp: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[float] = None
    contact_inbox: Optional[ContactInbox] = None
    meta: Optional[Dict[str, Any]] = None
    messages: Optional[List[Dict[str, Any]]] = None
    changed_attributes: Optional[List[Dict[str, Any]]] = None


class MessageUpdated(BaseModel):
    event: Literal["message_updated"]
    id: int
    content: str
    message_type: Union[int, str]
    created_at: Union[int, str]
    updated_at: Optional[Union[int, str]] = None
    private: bool = False
    status: Optional[str] = None
    source_id: Optional[str] = None
    content_type: str = "text"
    content_attributes: Dict[str, Any] = {}
    sender: Optional[Union[Contact, Dict[str, Any]]] = None
    conversation: Optional[Union[Conversation, Dict[str, Any]]] = None
    account: Optional[Account] = None
    inbox: Optional[Inbox] = None
    additional_attributes: Dict[str, Any] = {}
    content_attributes: Optional[Dict[str, Any]] = None


class ContactUpdated(BaseModel):
    event: Literal["contact_updated"]
    id: int
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    thumbnail: str = ""
    blocked: bool = False
    identifier: Optional[str] = None
    additional_attributes: Dict[str, Any] = {}
    custom_attributes: Dict[str, Any] = {}
    avatar: Optional[str] = None
    account: Optional[Account] = None
    changed_attributes: Optional[List[Dict[str, Any]]] = None


class ConversationUpdated(BaseModel):
    event: Literal["conversation_updated"]
    id: int
    inbox_id: Optional[int] = None
    can_reply: Optional[bool] = None
    channel: Optional[str] = None
    status: Optional[str] = None
    unread_count: Optional[int] = None
    priority: Optional[str] = None
    labels: List[str] = []
    custom_attributes: Dict[str, Any] = {}
    additional_attributes: Dict[str, Any] = {}
    snoozed_until: Optional[Any] = None
    first_reply_created_at: Optional[Any] = None
    waiting_since: Optional[int] = None
    agent_last_seen_at: Optional[int] = None
    contact_last_seen_at: Optional[int] = None
    last_activity_at: Optional[int] = None
    timestamp: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[float] = None
    contact_inbox: Optional[ContactInbox] = None
    meta: Optional[Dict[str, Any]] = None
    messages: Optional[List[Dict[str, Any]]] = None
    changed_attributes: Optional[List[Dict[str, Any]]] = None


# Discriminated union for all webhook events
WebhookEvent = Annotated[
    Union[
        ContactCreated,
        WebwidgetTriggered,
        MessageCreated,
        ConversationCreated,
        MessageUpdated,
        ContactUpdated,
        ConversationUpdated,
    ],
    Field(discriminator="event"),
]

# TypeAdapter for validating webhook events
WebhookEventAdapter = TypeAdapter(WebhookEvent)


# do not delete this part of code <start>


class ConversationStatus(BaseModel):
    """Conversation status with optional snooze timestamp"""

    status: Literal["open", "resolved", "pending", "snoozed"]
    snoozed_until: Optional[int] = None


class ConversationPriority(BaseModel):
    """Conversation priority level"""

    priority: Literal["urgent", "high", "medium", "low", "none"]


class ConversationLabel(BaseModel):
    """Array of labels for conversation"""

    labels: List[str] = []


class ConversationCustomAttributes(BaseModel):
    """Custom attributes as key-value pairs"""

    custom_attributes: Dict[str, str] = {}


class ConversationParams(BaseModel):
    """Parameters for conversation operations"""

    account_id: int
    conversation_id: int
    status: Optional[ConversationStatus] = None
    priority: Optional[ConversationPriority] = None
    labels: Optional[ConversationLabel] = None
    custom_attributes: Optional[ConversationCustomAttributes] = None


# do not delete this part of code <end>
