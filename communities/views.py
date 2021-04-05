from django.utils import timezone

from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    IsAdminUser,
)
from core.shortcuts import get_object_or_404
from utils.constants import Const
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
    tools,
)


class ForumViewSet(ModelViewSet):
    serializer_class = serializers.ForumSerializer
    model = models.Forum
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.all()


class ForumUpdateViewSet(ForumViewSet):
    serializer_class = serializers.ForumUpdateSerializer

    def perform_destroy(self, instance):
        tools.destroy_forum(instance)


class ForumReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ForumListSerializer
    model = models.Forum
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.search(self.q)


class ThreadViewSet(ModelViewSet):
    serializer_class = serializers.ThreadSerializer
    model = models.Thread

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = tools.write_permission(self.forum)
        return [permission() for permission in permission_classes]


class ThreadUpdateViewSet(ThreadViewSet):
    serializer_class = serializers.ThreadUpdateSerializer

    def get_queryset(self):
        return self.model.objects.forum_name(
            self.kwargs[Const.QUERY_PARAM_FORUM]
        )

    def sync_update(self, instance, partial):
        instance.modified_at = timezone.now()

    def has_ownership(self, instance):
        if self.request.user == instance.user:
            return True
        else:
            return False

    def perform_delete(self, instance):
        tools.delete_thread(instance)


class ThreadReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ThreadSerializer
    model = models.Thread

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = tools.read_permission(self.forum)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.forum_name(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.request.user
        )


class ThreadListViewSet(ThreadReadOnlyViewSet):
    serializer_class = serializers.ThreadListSerializer

    def get_queryset(self):
        return self.model.objects.search(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.q
        )


class ThreadTrashViewSet(ThreadListViewSet):
    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.trash(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.q
        )
