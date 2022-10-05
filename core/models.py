"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


def profile_image_file_path(instance, filename):
    # generate file path for new recipe image
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'profile', filename)


class UserManager(BaseUserManager):
    # manger for users
    def create_user(self, email, password, **extra_field):
        # create, save, and return new user
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        # create and return superuser
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # user in the system
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    # recipe object
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_mentor = models.BooleanField(default=False)
    skills = models.ManyToManyField('Skill')
    languages = models.ManyToManyField('Language')
    messages = models.ManyToManyField('Message')
    schedules = models.ManyToManyField('Schedule')
    image = models.ImageField(null=True, upload_to=profile_image_file_path)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    # skill model
    name = models.CharField(max_length=255)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Language(models.Model):
    # language model
    name = models.CharField(max_length=255)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Message(models.Model):
    # message model
    type = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Schedule(models.Model):
    # schedule model
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField('Participant')

    def __str__(self):
        return self.title

class Participant(models.Model):
    name = models.CharField(max_length=255)
    schedules = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

