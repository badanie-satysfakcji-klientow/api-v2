from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    class UserType(models.IntegerChoices):
        INTERVIEWEE = (1, 'Interviewee')
        CREATOR = (2, 'Creator')

    email = models.EmailField(max_length=320, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=UserType.choices, default=UserType.INTERVIEWEE)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        # update that later
        pass
