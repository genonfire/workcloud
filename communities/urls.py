from django.urls import path

from . import views

app_name = 'communities'

urlpatterns = [
    path(
        'forum/', views.ForumViewSet.as_view({
            'post': 'create',
        }), name='new_forum'
    ),
    path(
        'forum/<int:pk>/', views.ForumUpdateViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='forum'
    ),
    path(
        'forums/', views.ForumReadOnlyViewSet.as_view({
            'get': 'list',
        }), name='forums'
    ),
    path(
        'forums/<int:pk>/', views.ForumReadOnlyViewSet.as_view({
            'get': 'retrieve',
        }), name='retrieve_forum'
    ),
]
