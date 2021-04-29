import uuid

from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const
from utils.debug import Debug  # noqa


def app_directory_path(instance, filename):
    return 'files/{0}-{1}'.format(uuid.uuid4(), filename)


class AttachmentManager(models.Manager):
    def search(self, q):
        filename = Q()
        if q:
            filename = Q(file__icontains=q)
        return self.filter(filename)


class Attachment(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        related_name='attachment_user',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    file = models.FileField(
        upload_to=app_directory_path,
        max_length=Const.FILE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content_type = models.CharField(
        max_length=Const.FILE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    objects = AttachmentManager()

    class Meta:
        ordering = ('-id',)


class HolidayManager(models.Manager):
    def year(self, year):
        return self.filter(date__year=year)

    def date_exist(self, date):
        return self.filter(date=date).exists()


class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )

    objects = HolidayManager()

    class Meta:
        ordering = ['date']
