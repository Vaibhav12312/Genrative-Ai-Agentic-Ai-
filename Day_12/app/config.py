from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EPFOSathi"
    database_path: str = "data/epfosathi.db"
    llm_provider: str = "mock"
    openai_api_key: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
