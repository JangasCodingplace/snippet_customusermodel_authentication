import uuid
import os

from django.utils.timezone import now
from datetime import timedelta

from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise AttributeError('Users must have an email address')
        if not first_name:
            raise AttributeError('Users must have a first_name')
        if not last_name:
            raise AttributeError('Users must have an last_name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    first_name = models.CharField(
        max_length=60
    )
    last_name = models.CharField(
        max_length=60
    )
    is_admin = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    registration_date = models.DateTimeField(
        auto_now_add=True
    )
    activation_date = models.DateTimeField(
        blank=True,
        null=True
    )
    previous_version = None
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.is_active and (not self.activation_date or self.activation_date==''):
            self.activation_date = now()
        
        super().save(*args, **kwargs)
