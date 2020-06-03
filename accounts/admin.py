from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'call_name',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
    )
    search_fields = (
        'id',
        'username',
        'call_name',
        'first_name',
        'last_name',
    )
    ordering = (
        'id',
        'username',
    )
    list_display_links = (
        'id',
        'username',
        'call_name',
    )


@admin.register(models.LoginDevice)
class LoginDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'device',
        'os',
        'browser',
        'ip_address',
        'last_login',
        'is_registered',
    )
    search_fields = (
        'id',
        'user',
        'ip_address',
    )
    ordering = (
        'id',
        'user',
    )
    list_display_links = (
        'id',
        'user',
        'device',
    )
