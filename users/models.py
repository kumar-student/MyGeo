from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom manager for Custom User model
    """

    def get_by_natural_key(self, email):
        return super().get_by_natural_key(email)

    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(_('Email must be provided'))
        email = self.normalize_email(email)
        username = kwargs.get('username', None)
        if not username:
            username = email
        first_name = kwargs.pop('first_name', None)
        if not first_name:
            raise ValueError(_('First name must be provided'))
        last_name = kwargs.pop('last_name', None)
        user = self.model(email=email, **kwargs)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        return user

    def create_user(self, emial, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        return self._create_user(email, password, **kwargs)


class User(AbstractUser):
    """
    Custom user model
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    objects = UserManager()

    def __str__(self):
        return str(self.email)
