from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # z.ai API Configuration
    zai_api_key: str
    zai_model: str = "glm-4.7"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Agent Configuration
    agent_temperature: float = 0.7
    agent_max_tokens: int = 2000

    # Data directory
    data_dir: str = "data"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
