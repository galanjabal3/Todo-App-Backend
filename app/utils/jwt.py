import jwt
from datetime import datetime, timedelta, timezone
from app.config import config

def create_access_token(
    payload: dict = {},
    expired_in: int | None = 1,
):
    now = datetime.now(timezone.utc)

    payload = {
        **payload,
        "exp": now + timedelta(days=expired_in),
        "iss": "todo-app",
    }

    token = jwt.encode(
        payload,
        config.JWT_SECRET,
        algorithm="HS256",
    )

    return token
