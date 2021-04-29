from django.urls import path

from . import views

app_name = 'things'

urlpatterns = [
    path(
        'file/', views.AttachmentViewSet.as_view({
            'post': 'create',
        }), name='file_upload'
    ),
    path(
        'file/<int:pk>/', views.AttachmentViewSet.as_view({
            'delete': 'destroy',
        }), name='file_delete'
    ),
    path(
        'files/', views.AttachmentManageViewSet.as_view({
            'get': 'list',
        }), name='files_manage'
    ),
    path(
        'holiday/<int:pk>/', views.HolidayViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='holiday'
    ),
    path(
        'holidays/<int:year>/', views.HolidayYearViewSet.as_view({
            'post': 'update',
            'get': 'list',
        }), name='holidays'
    ),
]
