from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
    )
    log_file: str | None = Field(default=None, description="Log file path")

    # Chatwoot Configuration
    chatwoot_agent_bot_api_key: str | None = Field(
        default=None, description="Chatwoot Agent Bot API key"
    )
    chatwoot_user_api_key: str | None = Field(
        default=None, description="Chatwoot User API key"
    )
    chatwoot_base_url: str = Field(
        default="http://localhost:3000", description="Chatwoot Base URL"
    )

    # Letta Configuration
    letta_api_key: str | None = Field(default=None, description="Letta API key")
    letta_base_url: str = Field(
        default="http://localhost:8283", description="Letta Base URL"
    )
    letta_agent_id: str | None = Field(default=None, description="Letta Agent ID")
    letta_model: str = Field(
        default="anthropic/claude-sonnet-4-5-20250929", description="Letta model"
    )
    letta_embedding: str = Field(
        default="openai/text-embedding-3-small", description="Letta embedding model"
    )
    letta_agent_persona: str = Field(
        default="""I am a customer support assistant. I help customers by answering questions and providing interactive options.

I always use the send_chatwoot_message tool to reply to customers. I never respond with plain text.

I can send interactive messages:
- text: Simple text response
- input_select: Options menu with items like [{"title": "Option", "value": "option"}]
- form: Data collection form
- cards: Product cards with media and actions
- article: Knowledge base articles

I should choose the appropriate message type based on the customer's needs.""",
        description="Default persona for new agents",
    )

    # Webhook Configuration
    webhook_port: int = Field(default=8111, description="Webhook port")
    webhook_endpoint: str = Field(default="/webhook", description="Webhook endpoint")


settings = Settings()
