import jwt
from falcon import HTTPUnauthorized, HTTPForbidden

from app.config import config
from app.utils.logger import logger


EXCLUDE_PATHS = (
    "/apidoc",
    "/swagger", 
    "/openapi",
    "/favicon.ico"
)

class JWTMiddleware:
    def __init__(self, secret=None, algorithm="HS256"):
        self.secret = secret or config.JWT_SECRET
        self.algorithm = algorithm
        
    def process_request(self, req, resp):
        if req.path.startswith(EXCLUDE_PATHS):
            req.context["skip_auth"] = True
            return

    def process_resource(self, req, resp, resource, params):
        # Skip auth for public routes
        if req.context.get("skip_auth"):
            return
        
        if getattr(resource, "skip_auth", False):
            return

        auth_header = req.get_header("Authorization")
        if not auth_header:
            raise HTTPUnauthorized(
                title="Unauthorized",
                description="Missing Authorization header"
            )

        try:
            scheme, token = auth_header.split(" ")
            if scheme.lower() != "bearer":
                raise ValueError("Invalid auth scheme")
        except ValueError:
            raise HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid Authorization header format"
            )

        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise HTTPUnauthorized(
                title="Unauthorized",
                description="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid token"
            )

        # Inject ke request context
        req.context["user"] = payload
