from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissons import IsAdmin


class AdminView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"detail": "Hello, admin!"})


class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "Hello, user!"})
