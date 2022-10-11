"""
urls for recipe APIs 
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from userprofile import views

router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)
router.register('skills', views.SkillViewSet)
router.register('languages', views.LanguageViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
