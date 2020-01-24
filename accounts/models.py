from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models
from django.utils import timezone

from utils.constants import Const

from . import tools


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):
    username = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True
    )
    call_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True
    )
    # For later use such as Email confirmation
    is_approved = models.BooleanField(default=False)

    objects = UserManager()

    @classmethod
    def get_email_field_name(cls):
        """
        Do not use. Only For Django PasswordResetForm

        Check django.contrib.auth.forms.PasswordResetForm
        """
        return cls.USERNAME_FIELD

    def token(self):
        return tools.get_auth_token(self)

    def key(self):
        return self.token().key


class LoginDeviceManager(models.Manager):
    pass


class LoginDevice(models.Model):
    user = models.ForeignKey(
        'User',
        related_name="device_user",
        on_delete=models.CASCADE,
        null=True
    )
    device = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True
    )
    os = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True
    )
    browser = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True
    )
    ip_address = models.CharField(
        max_length=Const.IP_ADDRESS_MAX_LENGTH,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField(default=False)

    objects = LoginDeviceManager()

    class Meta:
        ordering = ('-id',)
