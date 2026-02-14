# Event types and their payload schema
## 1. event.contact_created
```json
{
  "account": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "additional_attributes": {},
  "avatar": "",
  "custom_attributes": {},
  "email": null,
  "id": 6,
  "identifier": null,
  "name": "morning-rain-190",
  "phone_number": null,
  "thumbnail": "",
  "blocked": false,
  "event": "contact_created"
}
```
## 2. event.webwidget_triggered
```json
{
  "id": 6,
  "contact": {
    "account": {
      "id": 1,
      "name": "Famiglia Land Realty"
    },
    "additional_attributes": {},
    "avatar": "",
    "custom_attributes": {},
    "email": null,
    "id": 6,
    "identifier": null,
    "name": "morning-rain-190",
    "phone_number": null,
    "thumbnail": "",
    "blocked": false
  },
  "inbox": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "account": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "current_conversation": null,
  "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
  "event": "webwidget_triggered",
  "event_info": {
    "initiated_at": {
      "timestamp": "Fri Feb 13 2026 09:23:04 GMT+0800 (Singapore Standard Time)"
    },
    "referer": "http://localhost:3001/",
    "widget_language": "en",
    "browser_language": "en",
    "browser": {
      "browser_name": "Microsoft Edge",
      "browser_version": "144.0.0.0",
      "device_name": "Unknown",
      "platform_name": "Windows",
      "platform_version": "10.0"
    }
  }
}
```
## 3. event.message_created
```json
{
  "account": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "additional_attributes": {},
  "content_attributes": {},
  "content_type": "input_email",
  "content": "<p>Get notified by email</p>\n",
  "conversation": {
    "additional_attributes": {
      "browser": {
        "device_name": "Unknown",
        "browser_name": "Microsoft Edge",
        "platform_name": "Windows",
        "browser_version": "144.0.0.0",
        "platform_version": "10.0"
      },
      "referer": "http://localhost:3001/",
      "initiated_at": {
        "timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800 (Singapore Standard Time)"
      },
      "browser_language": "en"
    },
    "can_reply": true,
    "channel": "Channel::WebWidget",
    "contact_inbox": {
      "id": 6,
      "contact_id": 6,
      "inbox_id": 1,
      "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
      "created_at": "2026-02-13T01:22:43.692Z",
      "updated_at": "2026-02-13T01:22:43.692Z",
      "hmac_verified": false,
      "pubsub_token": "Phu3WoxwKg8PnLo5CaVhJGLv"
    },
    "id": 6,
    "inbox_id": 1,
    "messages": [
      {
        "id": 103,
        "content": "Get notified by email",
        "account_id": 1,
        "inbox_id": 1,
        "conversation_id": 6,
        "message_type": 3,
        "created_at": 1770946053,
        "updated_at": "2026-02-13T01:27:33.365Z",
        "private": false,
        "status": "sent",
        "source_id": null,
        "content_type": "input_email",
        "content_attributes": {},
        "sender_type": null,
        "sender_id": null,
        "external_source_ids": {},
        "additional_attributes": {},
        "processed_message_content": "Get notified by email",
        "sentiment": {},
        "conversation": {
          "assignee_id": null,
          "unread_count": 1,
          "last_activity_at": 1770946053,
          "contact_inbox": {
            "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324"
          }
        }
      }
    ],
    "labels": [],
    "meta": {
      "sender": {
        "additional_attributes": {},
        "custom_attributes": {},
        "email": null,
        "id": 6,
        "identifier": null,
        "name": "morning-rain-190",
        "phone_number": null,
        "thumbnail": "",
        "blocked": false,
        "type": "contact"
      },
      "assignee": null,
      "assignee_type": null,
      "team": null,
      "hmac_verified": false
    },
    "status": "open",
    "custom_attributes": {},
    "snoozed_until": null,
    "unread_count": 1,
    "first_reply_created_at": null,
    "priority": null,
    "waiting_since": 1770946052,
    "agent_last_seen_at": 0,
    "contact_last_seen_at": 0,
    "last_activity_at": 1770946053,
    "timestamp": 1770946053,
    "created_at": 1770946052,
    "updated_at": 1770946053.366333
  },
  "created_at": "2026-02-13T01:27:33.365Z",
  "id": 103,
  "inbox": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "message_type": "template",
  "private": false,
  "sender": null,
  "source_id": null,
  "event": "message_created"
}
```
### 4. event.conversation_created
```json
{
  "additional_attributes": {
    "browser": {
      "device_name": "Unknown",
      "browser_name": "Microsoft Edge",
      "platform_name": "Windows",
      "browser_version": "144.0.0.0",
      "platform_version": "10.0"
    },
    "referer": "http://localhost:3001/",
    "initiated_at": {
      "timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800 (Singapore Standard Time)"
    },
    "browser_language": "en"
  },
  "can_reply": true,
  "channel": "Channel::WebWidget",
  "contact_inbox": {
    "id": 6,
    "contact_id": 6,
    "inbox_id": 1,
    "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
    "created_at": "2026-02-13T01:22:43.692Z",
    "updated_at": "2026-02-13T01:22:43.692Z",
    "hmac_verified": false,
    "pubsub_token": "Phu3WoxwKg8PnLo5CaVhJGLv"
  },
  "id": 6,
  "inbox_id": 1,
  "messages": [
    {
      "id": 103,
      "content": "Get notified by email",
      "account_id": 1,
      "inbox_id": 1,
      "conversation_id": 6,
      "message_type": 3,
      "created_at": 1770946053,
      "updated_at": "2026-02-13T01:27:33.365Z",
      "private": false,
      "status": "sent",
      "source_id": null,
      "content_type": "input_email",
      "content_attributes": {},
      "sender_type": null,
      "sender_id": null,
      "external_source_ids": {},
      "additional_attributes": {},
      "processed_message_content": "Get notified by email",
      "sentiment": {},
      "conversation": {
        "assignee_id": null,
        "unread_count": 1,
        "last_activity_at": 1770946052,
        "contact_inbox": {
          "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324"
        }
      }
    }
  ],
  "labels": [],
  "meta": {
    "sender": {
      "additional_attributes": {},
      "custom_attributes": {},
      "email": null,
      "id": 6,
      "identifier": null,
      "name": "morning-rain-190",
      "phone_number": null,
      "thumbnail": "",
      "blocked": false,
      "type": "contact"
    },
    "assignee": null,
    "assignee_type": null,
    "team": null,
    "hmac_verified": false
  },
  "status": "open",
  "custom_attributes": {},
  "snoozed_until": null,
  "unread_count": 1,
  "first_reply_created_at": null,
  "priority": null,
  "waiting_since": 1770946052,
  "agent_last_seen_at": 0,
  "contact_last_seen_at": 0,
  "last_activity_at": 1770946052,
  "timestamp": 1770946052,
  "created_at": 1770946052,
  "updated_at": 1770946052.947912,
  "event": "conversation_created"
}
```
### 5. event.message_updated
```json
{
  "account": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "additional_attributes": {},
  "content_attributes": {},
  "content_type": "text",
  "content": "<p>Give the team a way to reach you.</p>\n",
  "conversation": {
    "additional_attributes": {
      "browser": {
        "device_name": "Unknown",
        "browser_name": "Microsoft Edge",
        "platform_name": "Windows",
        "browser_version": "144.0.0.0",
        "platform_version": "10.0"
      },
      "referer": "http://localhost:3001/",
      "initiated_at": {
        "timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800 (Singapore Standard Time)"
      },
      "browser_language": "en"
    },
    "can_reply": true,
    "channel": "Channel::WebWidget",
    "contact_inbox": {
      "id": 6,
      "contact_id": 6,
      "inbox_id": 1,
      "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
      "created_at": "2026-02-13T01:22:43.692Z",
      "updated_at": "2026-02-13T01:22:43.692Z",
      "hmac_verified": false,
      "pubsub_token": "Phu3WoxwKg8PnLo5CaVhJGLv"
    },
    "id": 6,
    "inbox_id": 1,
    "messages": [
      {
        "id": 103,
        "content": "Get notified by email",
        "account_id": 1,
        "inbox_id": 1,
        "conversation_id": 6,
        "message_type": 3,
        "created_at": 1770946053,
        "updated_at": "2026-02-13T01:27:33.365Z",
        "private": false,
        "status": "sent",
        "source_id": null,
        "content_type": "input_email",
        "content_attributes": {},
        "sender_type": null,
        "sender_id": null,
        "external_source_ids": {},
        "additional_attributes": {},
        "processed_message_content": "Get notified by email",
        "sentiment": {},
        "conversation": {
          "assignee_id": null,
          "unread_count": 1,
          "last_activity_at": 1770946053,
          "contact_inbox": {
            "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324"
          }
        }
      }
    ],
    "labels": [],
    "meta": {
      "sender": {
        "additional_attributes": {},
        "custom_attributes": {},
        "email": null,
        "id": 6,
        "identifier": null,
        "name": "morning-rain-190",
        "phone_number": null,
        "thumbnail": "",
        "blocked": false,
        "type": "contact"
      },
      "assignee": null,
      "assignee_type": null,
      "team": null,
      "hmac_verified": false
    },
    "status": "open",
    "custom_attributes": {},
    "snoozed_until": null,
    "unread_count": 1,
    "first_reply_created_at": null,
    "priority": null,
    "waiting_since": 1770946052,
    "agent_last_seen_at": 0,
    "contact_last_seen_at": 1770946053,
    "last_activity_at": 1770946053,
    "timestamp": 1770946053,
    "created_at": 1770946052,
    "updated_at": 1770946053.837771
  },
  "created_at": "2026-02-13T01:27:33.358Z",
  "id": 102,
  "inbox": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "message_type": "template",
  "private": false,
  "sender": null,
  "source_id": null,
  "event": "message_updated"
}
```
### 6. event.contact_updated
```json
{
  "account": {
    "id": 1,
    "name": "Famiglia Land Realty"
  },
  "additional_attributes": {},
  "avatar": "",
  "custom_attributes": {},
  "email": null,
  "id": 6,
  "identifier": null,
  "name": "morning-rain-190",
  "phone_number": null,
  "thumbnail": "",
  "blocked": false,
  "event": "contact_updated",
  "changed_attributes": [
    {
      "updated_at": {
        "previous_value": "2026-02-13T01:22:43.582Z",
        "current_value": "2026-02-13T01:27:33.488Z"
      }
    },
    {
      "last_activity_at": {
        "previous_value": null,
        "current_value": "2026-02-13T01:27:33.485Z"
      }
    }
  ]
}
```
### 7. event.conversation_updated
```json
{
  "additional_attributes": {
    "browser": {
      "device_name": "Unknown",
      "browser_name": "Microsoft Edge",
      "platform_name": "Windows",
      "browser_version": "144.0.0.0",
      "platform_version": "10.0"
    },
    "referer": "http://localhost:3001/",
    "initiated_at": {
      "timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800 (Singapore Standard Time)"
    },
    "browser_language": "en"
  },
  "can_reply": true,
  "channel": "Channel::WebWidget",
  "contact_inbox": {
    "id": 6,
    "contact_id": 6,
    "inbox_id": 1,
    "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324",
    "created_at": "2026-02-13T01:22:43.692Z",
    "updated_at": "2026-02-13T01:22:43.692Z",
    "hmac_verified": false,
    "pubsub_token": "Phu3WoxwKg8PnLo5CaVhJGLv"
  },
  "id": 6,
  "inbox_id": 1,
  "messages": [
    {
      "id": 103,
      "content": "Get notified by email",
      "account_id": 1,
      "inbox_id": 1,
      "conversation_id": 6,
      "message_type": 3,
      "created_at": 1770946053,
      "updated_at": "2026-02-13T01:27:33.365Z",
      "private": false,
      "status": "sent",
      "source_id": null,
      "content_type": "input_email",
      "content_attributes": {},
      "sender_type": null,
      "sender_id": null,
      "external_source_ids": {},
      "additional_attributes": {},
      "processed_message_content": "Get notified by email",
      "sentiment": {},
      "conversation": {
        "assignee_id": null,
        "unread_count": 1,
        "last_activity_at": 1770946053,
        "contact_inbox": {
          "source_id": "ba7c30f6-7e6b-4ee5-a1e8-39a42778b324"
        }
      }
    }
  ],
  "labels": [],
  "meta": {
    "sender": {
      "additional_attributes": {},
      "custom_attributes": {},
      "email": null,
      "id": 6,
      "identifier": null,
      "name": "morning-rain-190",
      "phone_number": null,
      "thumbnail": "",
      "blocked": false,
      "type": "contact"
    },
    "assignee": null,
    "assignee_type": null,
    "team": null,
    "hmac_verified": false
  },
  "status": "open",
  "custom_attributes": {},
  "snoozed_until": null,
  "unread_count": 1,
  "first_reply_created_at": null,
  "priority": null,
  "waiting_since": 1770946052,
  "agent_last_seen_at": 0,
  "contact_last_seen_at": 1770946053,
  "last_activity_at": 1770946053,
  "timestamp": 1770946053,
  "created_at": 1770946052,
  "updated_at": 1770946053.629168,
  "event": "conversation_updated",
  "changed_attributes": [
    {
      "id": {
        "previous_value": null,
        "current_value": 6
      }
    },
    {
      "account_id": {
        "previous_value": null,
        "current_value": 1
      }
    },
    {
      "inbox_id": {
        "previous_value": null,
        "current_value": 1
      }
    },
    {
      "created_at": {
        "previous_value": null,
        "current_value": "2026-02-13T01:27:32.947Z"
      }
    },
    {
      "updated_at": {
        "previous_value": null,
        "current_value": "2026-02-13T01:27:32.947Z"
      }
    },
    {
      "contact_id": {
        "previous_value": null,
        "current_value": 6
      }
    },
    {
      "additional_attributes": {
        "previous_value": {},
        "current_value": {
          "browser_language": "en",
          "browser": {
            "browser_name": "Microsoft Edge",
            "browser_version": "144.0.0.0",
            "device_name": "Unknown",
            "platform_name": "Windows",
            "platform_version": "10.0"
          },
          "initiated_at": {
            "timestamp": "Fri Feb 13 2026 09:27:32 GMT+0800 (Singapore Standard Time)"
          },
          "referer": "http://localhost:3001/"
        }
      }
    },
    {
      "contact_inbox_id": {
        "previous_value": null,
        "current_value": 6
      }
    },
    {
      "uuid": {
        "previous_value": null,
        "current_value": "a0c688f0-b3b1-4ed1-bb25-ef375b828505"
      }
    },
    {
      "last_activity_at": {
        "previous_value": null,
        "current_value": "2026-02-13T01:27:32.940Z"
      }
    },
    {
      "waiting_since": {
        "previous_value": null,
        "current_value": "2026-02-13T01:27:32.947Z"
      }
    }
  ]
}
```
