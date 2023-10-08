from src.config.settings.base_settings import Settings
from dataclasses import dataclass, field
from typing import Optional

from src.config.enums import LOG_LEVELS, ENVIRONMENTS

@dataclass
class FlaskSettings(Settings):
    ''' 
        Class that holds the Flask application configuration
    '''

    GROUP_NAME = 'Flask'

    host: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_HOST", 
            data_type=str,
            default_value="0.0.0.0"
        ),
    ) # type: ignore

    port: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_PORT", 
            data_type=int,
            default_value="3000"
        ),
    ) # type: ignore

    env: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_ENV", 
            data_type=str,
            default_value=ENVIRONMENTS.DEVELOPMENT
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    debug_mode: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_DEBUG_MODE", 
            data_type=bool,
            default_value="True"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    enable_cors: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_ENABLE_CORS", 
            data_type=bool,
            default_value="True"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    cors_enabled_paths: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_CORS_ENABLED_PATHS", 
            data_type=list,
            default_value="/api/*"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore