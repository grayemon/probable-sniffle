# Development Diary

This document tracks the development progress, milestones, and decisions for the probable-sniffle project.

---

## 2026-02-16

**Milestone: Letta Integration Complete**

Replaced letta-client SDK with direct httpx calls due to SDK bug (ignores `streaming=False`).

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

## 2026-02-13

**Milestone: Webhook Processing Architecture**

Implemented event routing and handler extraction.

**Completed:**
- [x] Extract event handlers to services/handlers.py
- [x] Refactor main.py as orchestrator
- [x] Basic webhook receiver working
- [x] Event routing functional
- [x] Pydantic v2 discriminated unions for webhook validation

---

## Backlog

**Priority 1: End-to-End Testing**
- [ ] Verify full flow with real Chatwoot conversation
- [ ] Test all webhook event types

**Priority 2: Error Handling**
- [ ] Add retry logic for transient failures
- [ ] Improve error messages

**Priority 3: Testing**
- [x] Add unit tests for handlers
- [ ] Add integration tests for full flow
