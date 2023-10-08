from jsonschema import ValidationError, validate

from src.config.settings.core.app_settings import AppSettings
from src.errors.schema_validation_error import SchemaValidationError


class JSON_Schema_Validator:
    ''' Base class for validating a JSONSchema against
        a passed request payload
    '''

    def __init__(self, url:str, json_schema:dict[str, dict], settings:AppSettings) -> None:
        self.url = url
        self.json_schema = json_schema
        self.settings = settings


    def validate_request(self, method:str, payload:dict):
        ''' Validate a request payload against the provided schema '''

        if method in self.json_schema:
            method_schema = self.json_schema[method].copy()
            try:
                validate(payload, method_schema)
            except ValidationError as e:
                error = SchemaValidationError(
                    self.url,
                    method,
                    self._parse_path(e),
                    method_schema
                )

                return error

        return False


    def _parse_path(self, error:ValidationError):
        if len(error.path):
            return str(error.path.pop())

        return None