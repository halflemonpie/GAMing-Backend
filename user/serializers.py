"""
Serializers for API View
"""

from django.contrib.auth import (get_user_model, authenticate)
from django.utils.translation import gettext as _
from numpy import require
from rest_framework import serializers
from core.models import (Message, Schedule, User)


class MessageSerializer(serializers.ModelSerializer):
    # serializer for Messages

    class Meta:
        model = Message
        fields = ['id','type', 'sender', 'receiver', 'created_time', 'text', 'is_read']
        read_only_fields = ['id']


# class ParticipantSerializer(serializers.ModelSerializer):
#     # serializer for participants

#     class Meta:
#         model = Participant
#         fields = ['id', 'name', 'event']
#         read_only_fields = ['id', 'event']


class ScheduleSerializer(serializers.ModelSerializer):
    # serializer for schedules

    class Meta:
        model = Schedule
        fields = ['id','title', 'description', 'start_time', 'end_time', 'participants']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, required=False)
    schedules = ScheduleSerializer(many = True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'full_name', 'messages', 'schedules']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def _get_or_create_messages(self, messages, user):
        # handle getting or creating messages
        auth_user = self.context['request'].user
        for message in messages:
            message_obj, created = Message.objects.get_or_create(
                user=auth_user,
                **message
            )
            user.messages.add(message_obj)

    def _get_or_create_schedules(self, schedules, user):
        # handle getting or creating schedules
        auth_user = self.context['request'].user
        for schedule in schedules:
            schedule_obj, created = Schedule.objects.get_or_create(
                user=auth_user,
                **schedule
            )
            user.schedules.add(schedule_obj)

    def create(self, validated_data):
        # create user with encrypted password
        # create a profile
        messages = validated_data.pop('messages', [])
        schedules = validated_data.pop('schedules', [])
        user = get_user_model().objects.create_user(**validated_data)
        self._get_or_create_messages(messages, user)
        self._get_or_create_schedules(schedules, user)

        # return get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # update user information and encrypted password
        password = validated_data.pop('password', None)
        messages = validated_data.pop('messages', None)
        schedules = validated_data.pop('schedules', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if messages is not None:
            instance.messages.clear()
            self._get_or_create_messages(messages, instance)

        if schedules is not None:
            instance.schedules.clear()
            self._get_or_create_schedules(schedules, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return user


    # def create(self, validated_data):

    # def update(self, instance, validated_data):
    #     # update user


    #     return instance


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        # validate and authenticate the user
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
