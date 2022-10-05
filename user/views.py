"""
views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (UserSerializer, AuthTokenSerializer)
from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
    # create a new user in the system
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class CreateTokenView(ObtainAuthToken):
    # create a new auth token for user
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManagerUserView(generics.RetrieveUpdateAPIView):
    # manage the authenticated user
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # retrieve and return the authenticated user
        return self.request.user
