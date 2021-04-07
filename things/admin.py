from django.contrib import admin

from . import models


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'content_type',
        'size',
        'user',
        'created_at',
    )
    search_fields = (
        'file',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'file',
    )
