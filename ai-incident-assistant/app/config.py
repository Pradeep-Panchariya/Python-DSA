from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    app_name : str = "AI Incident Assistant"
    app_version : str = "0.1.0"
    environment : str = 'development'
    log_level : str = "INFO"

    # anthropic_api_key : str | None = None
    # anthropic_model : str = "claude-sonnet-4-7"
    # anthropic_workspace_id : str | None = None

    #gemini info 
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()