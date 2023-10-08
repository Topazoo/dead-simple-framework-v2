from typing import Optional
from flask import Flask, jsonify
from src.config.settings.core.app_settings import AppSettings
from src.config.settings.core.route_settings import AppRoutes
from src.errors.request_handling_error import Request_Handling_Error
from src.responses.api_error_response import API_Error_Response
from src.routing.route import Route
    
class Application:
    ''' Base application class that serves as a configuration class around Flask
        It allows us to extend the Flask application and add custom setup steps
        for our application like connecting to a database
    '''
    
    def __init__(self, routes:AppRoutes, settings:Optional[AppSettings]=None):
        # Get registered routes and settings
        self.routes = routes
        self.settings = settings or AppSettings()

        self.app = Flask(__name__)
        self._initialize()


    def _initialize(self):
        # Create error handling definitions
        self._register_error_handlers()

        # Register all passed Route definitions
        self.routes.register_routes(self.app)


    def _register_error_handlers(self):
        ''' Register wrappers to handle specific kinds of errors '''

        @self.app.errorhandler(API_Error_Response)
        def handle_user_thrown_error(error:API_Error_Response):
            response = jsonify(message=error.message)
            response.status_code = error.code
            return response
        
        @self.app.errorhandler(Request_Handling_Error)
        def handle_request_exception(error:Request_Handling_Error):
            response = jsonify(message=str(error))
            response.status_code = error.status_code
            return response


    def run(self):
        flask_settings = self.settings.flask
        self.app.run(
            host=flask_settings.host,
            port=flask_settings.port,
            debug=flask_settings.debug_mode,
        )