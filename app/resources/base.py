import falcon
import json
from pydantic import ValidationError
from itertools import chain
from app.config.spectree import api_spec, Response
from app.utils.logger import logger


class HealthResource:
    skip_auth = True
    
    @api_spec.validate(security=[])
    def on_get(self, req, resp):
        resp.media = {"status": "OK"}

class BaseResource:
    def parse_body(self, req, schema):
        try:
            data = schema(**req.media)
            return data.model_dump()  # ✅ Pydantic v2
        except ValidationError as e:
            logger.error(f"Err in parse_body: {e}")
            raise falcon.HTTPBadRequest(
                title="Validation error",
                description=e.errors(),
            )
    
    def resource_response(self, resp, message="Success", data=None, pagination=None, status=falcon.HTTP_200, metadata=None):
        resp.status = status
        resp.media = {
            "code": resp.status_code,
            "status": status,
            "message": message,
            "data": data,
        }
        if pagination:
            resp.media["pagination"] = pagination
        
        if metadata:
            resp.media["metadata"] = metadata

def generate_filters_resource(req=None, params_string=[], params_int=[], params_bool=[], params_list=[]):
    filters = []

    # Handle string and int parameters
    for param in chain(params_string, params_int):
        value = req.get_param(param, required=False, default="" if param in params_string else None)
        if value not in ["", None]:
            if param in params_int and value.isdigit():
                try:
                    value = int(value)
                except ValueError:
                    continue  # skip invalid int
            filters.append({"field": param, "value": value})
    
    # Handle boolean parameters
    for param in params_bool:
        value = req.get_param(param, required=False)
        if value is not None:
            value_str = str(value).strip().upper()
            if value_str == "TRUE" or value_str == "1":
                filters.append({"field": param, "value": True})
            elif value_str == "FALSE" or value_str == "0":
                filters.append({"field": param, "value": False})

    # Handle list parameters
    for param in params_list:
        value = req.get_param(param, required=False)
        if value:
            value = value.strip()
            items = []

            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    items = parsed
                else:
                    # parsed is a single item
                    items = [parsed]
            except json.JSONDecodeError:
                # Fallback: split by comma
                items = [v.strip() for v in value.split(",") if v.strip()]
                if not items:
                    items = [value]

            # If all are digit-like, convert to int
            if all(isinstance(item, str) and item.isdigit() for item in items):
                items = list(map(int, items))

            filters.append({"field": param, "value": items})

    return filters