import jwt
import uuid
import time
from django.conf import settings

ACCESS_TOKEN_LIFETIME = 60 * 15  # 15 minutes in seconds
REFRESH_TOKEN_LIFETIME = 60 * 60 * 24 * 7  # 7 days in seconds

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def _current_timestamp() -> int:
    """
    Returns the current timestamp as an integer.
    """
    return int(time.time())


def generate_tokens(user_id: int) -> tuple[str, str]:
    """
    Generates access and refresh JWT tokens for the given user ID.
    """
    now = _current_timestamp()

    # Create payload for the access token
    access_payload = {
        "type": "access",
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + ACCESS_TOKEN_LIFETIME,
    }

    # Create payload for the refresh token
    refresh_payload = {
        "type": "refresh",
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + REFRESH_TOKEN_LIFETIME,
    }

    # Encode payloads to generate JWT tokens
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def decode_token(token: str) -> dict:
    """
    Decodes a JWT token and returns its payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        # Token has expired
        raise jwt.ExpiredSignatureError("Token has expired") from e
    except jwt.InvalidTokenError as e:
        # Token is invalid
        raise jwt.InvalidTokenError("Invalid token") from e
