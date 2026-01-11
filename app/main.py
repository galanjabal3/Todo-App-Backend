import falcon
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from app.config.config import ENVIRONMENT
from app.config.spectree import api_spec
from app.utils.error_handlers import register_error_handlers
from app.utils.logger import logger
from app.routes.core import register_routes
from app.db.database import init_db
from app.middlewares.jwt_middleware import JWTMiddleware
from app.middlewares.cors_middleware import CORSMiddleware

import app.registry.service_registry   # ⬅️ registry di-load di sini
from app.container import ServiceContainer


def create_app():
    # Mark service container as ready AFTER all registry wiring is done
    ServiceContainer.boot()

    # Initialize Database
    init_db()

    app = falcon.App(middleware=[
        CORSMiddleware(),
        JWTMiddleware(),
    ])

    register_error_handlers(app) # Register error handlers
    register_routes(app) # Register Routes
    
    if ENVIRONMENT == "develop":
        api_spec.register(app) # Register app with SpecTree to generate Swagger

    logger.info("[STARTUP] Todo App Backend is starting in %s environment", ENVIRONMENT.capitalize())
    return app


app = create_app()
