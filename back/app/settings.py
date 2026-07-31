from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    database_url: str
    redis_url: str

    sender_email: str
    app_password: str
    smtp_host: str
    smtp_port: int

    allowed_domains: list[str]

    refresh_token_ttl_seconds: int

settings = Settings() # type: ignore