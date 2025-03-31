from rest_framework.generics import CreateAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from authentication.serializer import (
    RegisterSerializer,
    LoginSerializer,
    RefreshSerializer,
    LogoutSerializer,
)
from authentication.services.jwt_service import generate_tokens, decode_token
from authentication.services.token_service import TokenService

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    """
    API view for user registration.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(APIView):
    """
    API view for user login. Authenticates credentials using LoginSerializer and returns JWT tokens.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access, refresh = generate_tokens(user.id)
        payload = decode_token(refresh)
        jti = payload["jti"]
        exp = payload["exp"]

        TokenService.add_to_whitelist(jti, exp)

        return Response(
            {"access": access, "refresh": refresh},
            status=status.HTTP_200_OK,
        )


class RefreshAPIView(APIView):
    """
    API view to refresh JWT tokens using a valid refresh token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.context.get("payload")
        jti = payload["jti"]
        exp = payload["exp"]
        user_id = int(payload["sub"])

        # Invalidate the old refresh token
        TokenService.add_to_blacklist(jti, exp)
        TokenService.remove_from_whitelist(jti)

        # Generate new tokens
        access, new_refresh = generate_tokens(user_id)
        new_payload = decode_token(new_refresh)
        TokenService.add_to_whitelist(new_payload["jti"], new_payload["exp"])

        return Response(
            {"access": access, "refresh": new_refresh},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    """
    API view for user logout. Invalidates the provided refresh token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.context.get("payload")
        jti = payload["jti"]
        exp = payload["exp"]

        # Invalidate the refresh token by adding it to the blacklist and removing it from the whitelist
        TokenService.add_to_blacklist(jti, exp)
        TokenService.remove_from_whitelist(jti)

        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
