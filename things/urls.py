from django.urls import path

from . import views

app_name = 'things'

urlpatterns = [
    path(
        'file/upload/', views.AttachmentViewSet.as_view({
            'post': 'create',
        }), name='file_upload'
    ),
    path(
        'file/<int:pk>/', views.AttachmentViewSet.as_view({
            'delete': 'destroy',
        }), name='file_delete'
    ),
    path(
        'files/<str:app>/<int:key>/', views.AttachmentListViewSet.as_view({
            'get': 'list',
        }), name='files'
    ),
    path(
        'files/', views.AttachmentManageViewSet.as_view({
            'get': 'list',
        }), name='files_manage'
    ),
]
