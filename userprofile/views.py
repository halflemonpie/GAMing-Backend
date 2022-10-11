"""
views for the recipe APIs
"""

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Profile, Skill, Language, Message, Schedule, Participant)
from userprofile import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'skills',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter',
            ),
            OpenApiParameter(
                'languages',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filer',
            )
        ]
    )
)

class ProfileViewSet(viewsets.ModelViewSet):
    # view for manage recipe APIs
    serializer_class = serializers.ProfileDetailSerializer
    queryset = Profile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        # convert a list of strings to integers
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        # retrieve recipes for authenticated user
        skills = self.request.query_params.get('skills')
        languages = self.request.query_params.get('languages')
        queryset = self.queryset
        if skills:
            skill_ids = self._params_to_ints(skills)
            queryset = queryset.filter(skills__id__in=skill_ids)
        if languages:
            language_ids = self._params_to_ints(languages)
            queryset = queryset.filter(languages__id__in=language_ids)

        return queryset.order_by('-id').distinct()

    def get_serializer_class(self):
        # return the serializer class fro request
        if self.action == 'list':
            return serializers.ProfileSerializer
        elif self.action == 'upload_image':
            return serializers.ProfileImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        # create a new recipe
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        # upload an image to recipe
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, 
                enum=[0, 1],
                description='Filter by items assigned to profile.'
            )
        ]
    )
)
class BaseProfileAttrViewSet(mixins.DestroyModelMixin,
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
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.order_by('-name').distinct()


class SkillViewSet(BaseProfileAttrViewSet):
    # manage tags in database
    serializer_class = serializers.SkillSerializer
    queryset = Skill.objects.all()


class LanguageViewSet(BaseProfileAttrViewSet):
    # manage ingredients in the database
    serializer_class = serializers.LanguageSerializer
    queryset = Language.objects.all()

