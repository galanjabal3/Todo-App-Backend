import falcon
from app.resources.base import BaseResource, spec, Response, generate_filters_resource
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponseSpecTree

class UserResource(BaseResource):
    def __init__(self):
        self.service = UserService()

    @spec.validate(resp=Response(HTTP_200=UserResponseSpecTree))
    def on_get(self, req, resp):
        filters = generate_filters_resource(req, params_string=["email"])
        self.resource_response(resp=resp, data=self.service.get_all_with_filters(filters=filters))
        
        