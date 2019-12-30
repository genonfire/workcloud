from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'call_name',
        'last_login',
        'date_joined',
        'is_active',
        'is_staff'
    )
    search_fields = (
        'id',
        'username',
        'call_name',
        'first_name',
        'last_name'
    )
    ordering = (
        'id',
        'username'
    )
    list_display_links = (
        'id',
        'username',
        'call_name'
    )
