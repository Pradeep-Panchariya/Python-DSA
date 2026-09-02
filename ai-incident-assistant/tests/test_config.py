from app.config import settings

def test_default_settings():

    assert settings.app_name == "AI Incident Assistant"
    assert settings.app_version == "0.1.0"
    assert settings.environment == 'development'
    assert settings.log_level == "INFO"