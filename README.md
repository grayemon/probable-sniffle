# probable-sniffle

A Chatwoot-Letta integration Python webapp that enables AI-powered customer messaging.

## Overview

This application receives webhooks from Chatwoot, forwards customer messages to Letta AI, and sends AI-generated responses back to Chatwoot.

## Features

- FastAPI webhook receiver for Chatwoot events
- Letta AI integration for intelligent responses
- Conversation state management (stores Letta conversation IDs in Chatwoot)
- Support for multiple Chatwoot event types
- Comprehensive error handling and logging

## Architecture

```
Chatwoot --webhook--> FastAPI App --message--> Letta AI
    ^                                          |
    |__________response________________________|
```

### Flow
1. Chatwoot sends webhook to FastAPI app
2. Webhook validated via Pydantic discriminated unions
3. Event routed to appropriate handler
4. For incoming messages:
   - Create or retrieve Letta conversation
   - Send message to Letta
   - Extract assistant response
   - Send response back to Chatwoot

### Project Structure

```
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
LETTA_AGENT_ID=your_agent_id

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

## Tech Stack

- **Python 3.12+** - Primary language
- **FastAPI** - Web framework
- **uvicorn** - ASGI server
- **Pydantic v2** - Data validation
- **httpx** - HTTP client
- **uv** - Package manager
- **pytest** - Testing framework (dev)

---

## Development Diary

### 2026-02-16

**Milestone: Letta Integration Complete**

Replaced the letta-client SDK with direct httpx calls due to SDK bug (ignores `streaming=False`).

**Completed:**
- [x] Letta service implementation using direct httpx via APIClient
- [x] Message forwarding to Letta API
- [x] Response extraction from Letta responses
- [x] Added timeout support to APIClient (30s default, 60s for Letta)
- [x] Added query params support to APIClient POST method
- [x] Cleaned up tests folder (removed 11 outdated files)
- [x] Refactored logging to use centralized config from .env
- [x] Migrated from requirements.txt to pyproject.toml
- [x] Added unit tests for handlers (17 tests)

**Commits:**
- `939185f` feat: Replace letta-client SDK with direct httpx calls, add APIClient improvements, and cleanup tests
- `6dfb9c5` docs: Update letta_memory_export.json with current project state
- `c242969` test: Add unit tests for services/handlers.py

---

### 2026-02-13

**Milestone: Webhook Processing Architecture**

Implemented event routing and handler extraction.

**Completed:**
- [x] Extract event handlers to services/handlers.py
- [x] Refactor main.py as orchestrator
- [x] Basic webhook receiver working
- [x] Event routing functional
- [x] Pydantic v2 discriminated unions for webhook validation

---

### Backlog

**Priority 1: End-to-End Testing**
- [ ] Verify full flow with real Chatwoot conversation
- [ ] Test all webhook event types

**Priority 2: Error Handling**
- [ ] Add retry logic for transient failures
- [ ] Improve error messages

**Priority 3: Testing**
- [x] Add unit tests for handlers
- [ ] Add integration tests for full flow
