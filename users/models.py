from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField as BasePhoneField

class PhoneField(BasePhoneField):
    pass


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
        first_name = kwargs.pop('first_name', None)
        if not first_name:
            raise ValueError(_('First name must be provided'))
        last_name = kwargs.pop('last_name', None)
        if not last_name:
            raise ValueError(_('Last name must be provided'))
        address = kwargs.pop('address', None)
        if not address:
            raise ValueError(_('Address must be provided'))
        phone = kwargs.pop('phone', None)
        if not phone:
            raise ValueError(_('Phone number must be provided'))
        location = kwargs.pop('location', None)
        if not location:
            raise ValueError(_('location must be provided'))
        user = self.model(email=email, **kwargs)
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.phone = phone
        user.location = location
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('location', Point(0.0, 0.0))
        if kwargs.get("is_staff") is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self._create_user(email, password, **kwargs)


class User(AbstractUser, PermissionsMixin):
    """
    Custom user model
    """
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    phone = PhoneField()
    location = models.PointField()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'address',
        'phone'
    ]

    def __str__(self):
        return str(self.email)
