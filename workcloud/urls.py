from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
