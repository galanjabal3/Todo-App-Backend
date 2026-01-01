import falcon
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from app.config.config import ENVIRONMENT
from app.utils.logger import logger
from app.utils.error_handlers import register_error_handlers

# Resource Entities
from app.resources.base import spec
from app.resources.user_resource import UserResource

app = falcon.App()

# Register error handlers
register_error_handlers(app)

app.add_route("/test", UserResource())

# Register your app with SpecTree to generate Swagger.
spec.register(app)

logger.info("[STARTUP] Todo App Backend is starting in %s environment", ENVIRONMENT.capitalize())