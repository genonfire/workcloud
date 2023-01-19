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


@admin.register(models.Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'name',
    )
    search_fields = (
        'date',
        'name',
    )
    ordering = (
        '-date',
    )
    list_display_links = (
        'date',
        'name',
    )


class OrderThingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'order',
        'thing_type',
    )
    search_fields = (
        'name',
    )
    ordering = (
        'order',
        'id',
    )
    list_display_links = (
        'name',
    )
