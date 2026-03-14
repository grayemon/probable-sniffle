# probable-sniffle

A Chatwoot-Letta integration Python webapp that enables AI-powered customer messaging.

## Overview

This application receives webhooks from Chatwoot, forwards customer messages to Letta AI, and sends AI-generated responses back to Chatwoot.

## Features

- FastAPI webhook receiver for Chatwoot events
- Letta AI integration with client-side tool execution
- Dynamic agent creation (one Letta agent per Chatwoot conversation)
- Interactive message support (options, forms, cards, articles)
- Conversation state management (stores Letta IDs in Chatwoot)
- Support for multiple Chatwoot event types
- Comprehensive error handling and logging

## Architecture

```text
Chatwoot --webhook--> Webapp --API--> Letta Agent
                         ^                   |
                         |        approval_request_message
                         +---execute tool----+
                         |                   |
                         +---send result---->+
                                             v
                                    Chatwoot API (reply)
```

### Flow

1. Chatwoot sends webhook to FastAPI app
2. Webhook validated via Pydantic discriminated unions
3. Event routed to appropriate handler
4. For incoming messages:
   - Create or retrieve Letta agent (one per Chatwoot conversation)
   - Create or retrieve Letta conversation
   - Send message to Letta
   - Agent calls `send_chatwoot_message` tool (client-side execution)
   - Webapp executes tool locally (sends to Chatwoot)
   - Result sent back to agent

### Project Structure

```text
probable-sniffle/
├── main.py               # FastAPI entry point
├── config/settings.py    # Pydantic settings from .env
├── base/
│   ├── api_client.py     # Generic async HTTP client
│   └── models.py         # Pydantic webhook models
├── services/
│   ├── handlers.py       # Webhook event handlers
│   ├── letta.py          # Letta API integration
│   └── chatwoot.py       # Chatwoot API integration
├── utils/
│   ├── logger.py         # Logging setup
│   └── error_handler.py  # Error handling
├── docs/                 # Documentation
│   └── development_diary.md  # Development progress and decisions
├── tests/                # Test files
├── logs/                 # Log files
└── resources/            # API documentation
```

## Setup

### Requirements

- Python 3.12+
- uv package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd probable-sniffle

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### Configuration

Create a `.env` file with the following variables:

```env
# Letta Configuration
LETTA_API_KEY=your_letta_api_key
LETTA_BASE_URL=https://api.letta.com

# Optional: Override defaults for agent creation
# LETTA_MODEL=anthropic/claude-sonnet-4-5-20250929
# LETTA_EMBEDDING=openai/text-embedding-3-small
# LETTA_AGENT_PERSONA=I am a customer support assistant...

# Chatwoot Configuration
CHATWOOT_AGENT_BOT_API_KEY=your_bot_api_key
CHATWOOT_USER_API_KEY=your_user_api_key
CHATWOOT_BASE_URL=https://your-chatwoot-instance.com

# Webhook Configuration
WEBHOOK_PORT=8111
WEBHOOK_ENDPOINT=webhook

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/chatwoot-letta.log
```

> **Note:** Agents are created dynamically per Chatwoot conversation. You don't need to specify `LETTA_AGENT_ID`.

### Running

```bash
# Start the webhook server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --port 8111
```

## Development

### Commands

```bash
# Install dependencies
uv sync

# Run tests
python -m tests.letta_service_test
python -m tests.letta_create_conversation
python -m tests.chatwoot

# Run webhook tester (requires running server)
python -m tests.webhook_tester
```

### Supported Webhook Events

| Event | Status |
|-------|--------|
| message_created | Implemented |
| message_updated | Implemented |
| webwidget_triggered | Implemented |
| contact_created | Acknowledged |
| contact_updated | Acknowledged |
| conversation_created | Acknowledged |
| conversation_updated | Acknowledged |

### Interactive Messages

The Letta agent can send interactive message types to Chatwoot:

| Type | Description |
|------|-------------|
| `text` | Simple text response |
| `input_select` | Options menu with selectable items |
| `form` | Data collection form with fields |
| `cards` | Product cards with media and actions |
| `article` | Knowledge base articles |

See [Chatwoot Interactive Messages](https://www.chatwoot.com/hc/user-guide/articles/1677689344-how-to-use-interactive-messages) for payload examples.

## Tech Stack

- **Python 3.12+** - Primary language
- **FastAPI** - Web framework
- **uvicorn** - ASGI server
- **Pydantic v2** - Data validation
- **httpx** - HTTP client
- **uv** - Package manager
- **pytest** - Testing framework (dev)

## Documentation

- **Development Diary** - See [docs/development_diary.md](docs/development_diary.md) for detailed development progress, milestones, and decisions.
