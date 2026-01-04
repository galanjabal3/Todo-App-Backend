from spectree import SpecTree, SecurityScheme, Response
from spectree.plugins.falcon_plugin import FalconPlugin

api_spec = SpecTree(
    "falcon",
    backend=FalconPlugin,
    title="Todo App API",
    description="A Todo application API",
    version="1.0.0",
    security_schemes=[
        SecurityScheme(
            name="jwt",
            data={
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        )
    ],
    security=[
        {"jwt": []}
    ],
    tags=[
        {"name": "Auth", "description": "Authentication APIs"},
        {"name": "User", "description": "User APIs"},
    ],
)
