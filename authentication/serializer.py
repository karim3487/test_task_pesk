from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from authentication.services.jwt_service import decode_token
from authentication.services.token_service import TokenService

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        """
        Validate user credentials and return the authenticated user.
        """
        request = self.context.get("request")
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request=request, email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value):
        """
        Validate the refresh token:
        - Ensure token can be decoded without errors.
        - Check that the token type is 'refresh'.
        - Verify token is not blacklisted and is in the whitelist.
        """
        try:
            payload = decode_token(value)
        except ExpiredSignatureError:
            raise serializers.ValidationError("Token has expired")
        except InvalidTokenError:
            raise serializers.ValidationError("Invalid token")

        if payload.get("type") != "refresh":
            raise serializers.ValidationError("Invalid token type")

            # Save payload for use in the view
        self.context["payload"] = payload
        return value


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value):
        """
        Validate the refresh token:
        - Ensure token can be decoded without errors.
        - Check that the token type is 'refresh'.
        - Verify token is not blacklisted and is in the whitelist.
        """
        try:
            payload = decode_token(value)
        except ExpiredSignatureError:
            raise serializers.ValidationError("Token has expired")
        except InvalidTokenError:
            raise serializers.ValidationError("Invalid token")

        if payload.get("type") != "refresh":
            raise serializers.ValidationError("Invalid token type")

        jti = payload.get("jti")

        if TokenService.is_blacklisted(jti):
            raise serializers.ValidationError("Token is blacklisted")
        if not TokenService.is_whitelisted(jti):
            raise serializers.ValidationError("Token is not in whitelist")

        # Save payload in the serializer context for later use in the view.
        self.context["payload"] = payload
        return value
