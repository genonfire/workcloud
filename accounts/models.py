from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models

from utils.constants import Const
from utils.debug import Debug  # noqa


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


class LoginDeviceManager(models.Manager):
    pass


class LoginDevice(models.Model):

    user = models.ForeignKey(
        'User',
        related_name="device_user",
        on_delete=models.CASCADE,
        null=True
    )

    objects = LoginDeviceManager()

    class Meta:
        ordering = ['-id']
