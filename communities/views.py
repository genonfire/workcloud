from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    IsAdminUser,
)

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
