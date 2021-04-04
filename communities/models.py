from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const


class OptionManager(models.Manager):
    pass


class Option(models.Model):
    is_active = models.BooleanField(default=True)
    permission_read = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    permission_write = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    permission_reply = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )

    objects = OptionManager()

    class Meta:
        ordering = ('id',)


class ForumManager(models.Manager):
    def search(self, q):
        if q:
            query = (
                Q(name__icontains=q) |
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(managers__username__iexact=q)
            )
        else:
            query = Q()
        return self.filter(query)


class Forum(models.Model):
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
        unique=True,
    )
    title = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True)
    managers = models.ManyToManyField(
        'accounts.User',
        related_name='forum_managers',
        default='',
        blank=True,
    )
    option = models.ForeignKey(
        'Option',
        related_name='forum_option',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = ForumManager()

    class Meta:
        ordering = ('-id',)

    def thread_count(self):
        return Thread.objects.forum(self).count()

    def reply_count(self):
        return Reply.objects.filter(thread__forum=self).count()


class ThreadManager(models.Manager):
    def forum(self, forum):
        return self.filter(forum=forum)


class Thread(models.Model):
    forum = models.ForeignKey(
        'Forum',
        related_name='thread_forum',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'accounts.User',
        related_name='thread_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # in case of anonymous
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=Const.TITLE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = ThreadManager()

    class Meta:
        ordering = ('-id',)


class ReplyManager(models.Manager):
    pass


class Reply(models.Model):
    thread = models.ForeignKey(
        'Thread',
        related_name='reply_thread',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reply_id = models.IntegerField(default=0)
    user = models.ForeignKey(
        'accounts.User',
        related_name='reply_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # in case of anonymous
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = ThreadManager()

    class Meta:
        ordering = ('-id',)
