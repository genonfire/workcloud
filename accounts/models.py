from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const

from . import tools


class UserManager(DjangoUserManager):
    def active(self):
        return self.filter(is_superuser=False).filter(is_active=True)

    def approved(self):
        return self.active().filter(is_approved=True)

    def staff(self):
        return self.approved().filter(is_staff=True)

    def staff_search(self, q):
        name = Q()
        if q:
            name = Q(username__icontains=q)
        return self.staff().filter(name)

    def user_serach(self, q):
        name = Q()
        if q:
            name = (
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(call_name__icontains=q) |
                Q(tel__icontains=q)
            )
        return self.approved().filter(name)


class User(AbstractUser):
    username = models.EmailField(
        unique=True,
    )
    first_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    call_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="photo/",
        max_length=Const.FILE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    tel = models.CharField(
        max_length=Const.TEL_MAX_LENGTH,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=Const.ADDRESS_MAX_LENGTH,
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        ordering = ['-id']

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
        related_name='device_user',
        on_delete=models.CASCADE,
        null=True,
    )
    device = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    os = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    browser = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    ip_address = models.CharField(
        max_length=Const.IP_ADDRESS_MAX_LENGTH,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField(default=False)

    objects = LoginDeviceManager()

    class Meta:
        ordering = ['-id']
