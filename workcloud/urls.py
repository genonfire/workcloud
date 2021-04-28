from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from utils.bot import (
    DailyBotView,
    MinuteBotView,
    MonthlyBotView,
)


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('bot/daily/', DailyBotView.as_view(), name='daily_bot'),
    path('bot/monthly/', MonthlyBotView.as_view(), name='monthly_bot'),
    path('bot/minute/', MinuteBotView.as_view(), name='minute_bot'),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path(
        'api/communities/',
        include('communities.urls', namespace='communities')
    ),
    path('api/things/', include('things.urls', namespace='things')),
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL_SERVER:
    urlpatterns += [
        path(
            'restapi/',
            include('rest_framework.urls', namespace='rest_framework')
        )
    ]

    if 'drf_yasg' in settings.INSTALLED_APPS:
        from rest_framework.permissions import AllowAny
        from drf_yasg.views import get_schema_view
        from drf_yasg import openapi

        schema_view = get_schema_view(
            openapi.Info(
                title="workcloud APIs",
                default_version='beta',
            ),
            public=True,
            permission_classes=(AllowAny,),
        )

        urlpatterns += [
            url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
                cache_timeout=0), name='schema-json'),
            url(r'^swagger/$', schema_view.with_ui(
                'swagger', cache_timeout=0), name='schema-swagger-ui'),
            url(r'^redoc/$', schema_view.with_ui(
                'redoc', cache_timeout=0), name='schema-redoc'),
        ]
