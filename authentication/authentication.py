import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        if jwt_token is None:
            return None

        if not jwt_token.startswith("Bearer "):
            return None

        jwt_token = CustomJWTAuthentication.get_the_token_from_header(
            jwt_token
        )  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Invalid signature")
        except Exception:
            raise ParseError()

        # Get the user from the database
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationFailed("User identifier not found in JWT")

        user = User.objects.filter(pk=user_id).first()
        if user is None:
            raise AuthenticationFailed("User not found")

        # Return the user and token payload
        return user, payload

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace("Bearer", "").replace(" ", "")  # clean the token
        return token
