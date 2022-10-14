"""
views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.models import Message, Schedule
from user.serializers import (UserSerializer, AuthTokenSerializer)
from django.contrib.auth import get_user_model

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (viewsets, mixins)
from user import serializers


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

class BaseUserAttrViewSet(  mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin, 
                            mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
    # base viewset for recipe attribute
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # filter queryset to authenticated user
        assigned_only = bool(int(self.request.query_params.get('assigned_only', 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(profile__isnull=False)

        return queryset.order_by('-id').distinct()

class MessageViewSet(BaseUserAttrViewSet):
    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()

class ScheduleViewSet(BaseUserAttrViewSet):
    serializer_class = serializers.ScheduleSerializer
    queryset = Schedule.objects.all()