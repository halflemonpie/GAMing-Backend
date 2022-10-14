"""
serializers for recipe APIs
"""

from rest_framework import serializers

from core.models import (Profile, Skill, Language)


class SkillSerializer(serializers.ModelSerializer):
    # serializer for ingredients

    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']

class LanguageSerializer(serializers.ModelSerializer):
    # serializer for tags

    class Meta:
        model = Language
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    # serializer for profiles
    skills = SkillSerializer(many=True, required=False)
    languages = LanguageSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'short_description', 'description', 'is_mentor', 'skills', 'languages']
        read_only_fields = ['id', 'user']

    def _get_or_create_skills(self, skills, profile):
        # handle getting or creating skills
        auth_user = self.context['request'].user
        for skill in skills:
            skill_obj, created = Skill.objects.get_or_create(
                user=auth_user,
                **skill
            )
            profile.skills.add(skill_obj)

    def _get_or_create_languages(self, languages, profile):
        # handle getting or creating languages
        auth_user = self.context['request'].user
        for language in languages:
            language_obj, created = Language.objects.get_or_create(
                user=auth_user,
                **language
            )
            profile.languages.add(language_obj)


    def create(self, validated_data):
        # create a profile
        skills = validated_data.pop('skills', [])
        languages = validated_data.pop('languages', [])
        profile = Profile.objects.create(**validated_data)
        self._get_or_create_skills(skills, profile)
        self._get_or_create_languages(languages, profile)

        return profile

    def update(self, instance, validated_data):
        # update recipe
        skills = validated_data.pop('skills', None)
        languages = validated_data.pop('languages', None)
        if skills is not None:
            instance.skills.clear()
            self._get_or_create_skills(skills, instance)

        if languages is not None:
            instance.languages.clear()
            self._get_or_create_languages(languages, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)


        
        instance.save()
        return instance



class ProfileDetailSerializer(ProfileSerializer):
    # profile detail serializer based on profile serializer

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields


class ProfileImageSerializer(serializers.ModelSerializer):
    # serializer for uploading images to recipes

    class Meta:
        model = Profile
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}



