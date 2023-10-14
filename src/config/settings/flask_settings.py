from flask import current_app, has_app_context
from src.config.enums.logs import LOG_GROUPS, LOG_LEVELS
from src.config.settings.base.base_settings import Settings
from dataclasses import dataclass, field
from typing import Optional

from src.config.enums import ENVIRONMENTS

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
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    port: Optional[int] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_PORT", 
            data_type=int,
            default_value="3000"
        ),
        metadata={"log_level": LOG_LEVELS.DEBUG}
    ) # type: ignore

    env: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_ENV", 
            data_type=str,
            default_value=ENVIRONMENTS.DEVELOPMENT
        ),
    ) # type: ignore

    debug_mode: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_DEBUG_MODE", 
            data_type=bool,
            default_value="True"
        ),
    ) # type: ignore

    requires_mongodb: Optional[bool] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_REQUIRES_MONGODB", 
            data_type=bool,
            default_value="False"
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    log_level: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_LOG_LEVEL", 
            data_type=str,
            default_value=LOG_LEVELS.WARN
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    config_log_level: Optional[str] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_CONFIG_LOG_LEVEL", 
            data_type=str,
            default_value=LOG_LEVELS.WARN
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore

    cors_origins: Optional[list] = field(
        default_factory=lambda: Settings.read_config_from_env_or_default(
            "APP_CORS_ORIGINS", 
            data_type=list,
            default_value=None
        ),
        metadata={"log_level": LOG_LEVELS.WARN}
    ) # type: ignore


    def __post_init__(self):
        if self.config_log_level:
            self._configure_logger(LOG_GROUPS.APP_CONFIG, self.config_log_level)

        self._set_default_cors_origins()
            
        super().__post_init__()

    
    def _set_default_cors_origins(self):
        if not self.cors_origins:
            self.cors_origins = [
                f"http://{self.host or ''}:{self.port or ''}",
                f"https://{self.host or ''}:{self.port or ''}"
            ]


    @classmethod
    def get_settings_from_flask(cls) -> Optional["FlaskSettings"]:
        ''' Get the Flask settings for the current Flask app '''

        if has_app_context():
            current_settings = current_app.config.get('APP_SETTINGS')
            if current_settings:
                return current_settings.flask