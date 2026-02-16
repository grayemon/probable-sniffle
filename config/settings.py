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

    # Webhook Configuration
    webhook_port: int = Field(default=8111, description="Webhook port")
    webhook_endpoint: str = Field(default="/webhook", description="Webhook endpoint")


settings = Settings()
