"""
Views for user APIs.
"""

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings

from rest_framework.permissions import IsAuthenticated
from core.permissions import AccessOwnerOnly

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class AuthTokenView(ObtainAuthToken):
    """Create auth token for an existing user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete user profile."""

    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, AccessOwnerOnly]

    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user
