from typing import Optional
from flask import Flask
from src.config.enums.log_levels import LOG_LEVELS
from src.config.settings.core.app_settings import AppSettings
from src.utils.logging.loggers.routing import RoutingLogger
from .route_handler import RouteHandler

class Route:
    ''' Base class that wraps Flasks normal routing allowing us
        to pick up configured parameters like the database to 
        connect to or the permissions required to access the 
        endpoint
    '''

    def __init__(self, 
            url:str, 
            handler:RouteHandler, 
            request_schema:Optional[dict]=None,
            log_level:str=LOG_LEVELS.WARN
        ):
        self.url = url
        self.handler = handler
        self.request_schema = request_schema or {}
        self.log_level = log_level
    
    
    def register(self, flask_app:Flask, settings:AppSettings):
        ''' Registers this URL to a Flask app and binds all supplied
            methods (e.g. GET or POST) specified in the passed RouteHandler
        '''

        self.handler.configure_logger(self.log_level)
        self.handler.register_url_methods(self.url, flask_app, settings, self.request_schema)
        RoutingLogger.info(f"Created application route: [{self.url}]")
