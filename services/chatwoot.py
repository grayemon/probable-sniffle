from utils.logger import setup_logger
from config.settings import settings
from base.api_client import APIClient
from base.models import ConversationParams
import json


class ChatwootService:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.client = APIClient(
            base_url=settings.chatwoot_base_url,
            auth_header_name="api_access_token",
            api_key=settings.chatwoot_user_api_key,
            auth_header_prefix=None,
        )

    # get conversation status
    async def get_conversation_status(self, params: ConversationParams):
        # get {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}
        self.logger.info(
            f"getting status of conversation {params.conversation_id} in account {params.account_id}"
        )
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}"
        response = await self.client.get(endpoint)
        status = response.get("status")
        self.logger.info(f"Status: {status}")
        return status

    # get conversation details
    async def get_conversation_details(self, params: ConversationParams):
        self.logger.info(
            f"getting details of conversation {params.conversation_id} in account {params.account_id}"
        )
        # get {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}"
        response = await self.client.get(endpoint)
        self.logger.info(f"Response: {json.dumps(response,indent=4)}")
        return response

    # toggle conversation status
    async def toggle_status(self, params: ConversationParams):
        self.logger.info(
            f"toggling status of conversation {params.conversation_id} in account {params.account_id}"
        )
        # {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}/toggle_status"

        response = await self.client.post(endpoint, data=params.status.model_dump())
        if response:
            self.logger.info(
                f"Response: {response.get('payload').get('current_status')}"
            )
        else:
            self.logger.info("Response: Empty response (status toggled successfully)")

    # get messages
    async def get_messages(self, params: ConversationParams):
        self.logger.info(
            f"getting messages of conversation {params.conversation_id} in account {params.account_id}"
        )
        # get {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}/messages"
        response = await self.client.get(endpoint)
        self.logger.info(f"Response: {json.dumps(response,indent=4)}")
        return response

    # send message
    async def send_message(self, params: ConversationParams, message: str):
        self.logger.info(
            f"sending message to conversation {params.conversation_id} in account {params.account_id}"
        )
        # post {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}/messages"
        # Try agent bot API key first, fallback to user API key on 401 error
        try:
            response = await self.client.post(
                endpoint,
                api_key=settings.chatwoot_agent_bot_api_key,
                data={"content": message},
            )
        except Exception as e:
            if "401" in str(e):
                self.logger.warning(
                    "Bot API key unauthorized, falling back to user API key"
                )
                response = await self.client.post(
                    endpoint,
                    api_key=settings.chatwoot_user_api_key,
                    data={"content": message},
                )
            else:
                raise
        if response:
            self.logger.info(f"Response: {json.dumps(response,indent=4)}")
        else:
            self.logger.info("Response: Empty response (message sent successfully)")
        return response

    # toggle priority
    async def toggle_priority(self, params: ConversationParams):
        self.logger.info(
            f"toggling priority of conversation {params.conversation_id} in account {params.account_id}"
        )
        # {base_url}/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}/toggle_priority"
        response = await self.client.post(endpoint, data=params.priority.model_dump())
        if response:
            self.logger.info(f"Response: {response.get("priority")}")
        else:
            self.logger.info("Response: Empty response (priority toggled successfully)")

    # update custom attributes
    async def update_custom_attributes(self, params: ConversationParams):
        self.logger.info(
            f"updating custom attributes of conversation {params.conversation_id} in account {params.account_id}"
        )
        # {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes
        endpoint = f"/api/v1/accounts/{params.account_id}/conversations/{params.conversation_id}/custom_attributes"
        response = await self.client.post(
            endpoint, data=params.custom_attributes.model_dump()
        )
        self.logger.info(f"Response: {json.dumps(response,indent=4)}")
        if response:
            self.logger.info(f"Response: {response.get("custom_attributes")}")
        else:
            self.logger.info(
                "Response: Empty response (custom attributes updated successfully)"
            )


chatwoot_service = ChatwootService()
