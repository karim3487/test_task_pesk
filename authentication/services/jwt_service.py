import jwt
import uuid
import time

from django.conf import settings


def generate_tokens(user_id: int) -> tuple[str, str]:
    """
    Generates access and refresh JWT tokens for the given user ID.
    """
    now = int(time.time())

    # Create payload for the access token
    access_payload = {
        "type": "access",
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + settings.ACCESS_TOKEN_LIFETIME,
    }

    # Create payload for the refresh token
    refresh_payload = {
        "type": "refresh",
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + settings.REFRESH_TOKEN_LIFETIME,
    }

    # Encode payloads to generate JWT tokens
    access_token = jwt.encode(
        access_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    refresh_token = jwt.encode(
        refresh_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return access_token, refresh_token


def decode_token(token: str) -> dict:
    """
    Decodes a JWT token and returns its payload.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        # Token has expired
        raise jwt.ExpiredSignatureError("Token has expired") from e
    except jwt.InvalidTokenError as e:
        # Token is invalid
        raise jwt.InvalidTokenError("Invalid token") from e
