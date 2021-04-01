from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    IsAdminUser,
    IsApproved,
)

from utils.constants import Const
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
    tools,
)


class AttachmentViewSet(ModelViewSet):
    serializer_class = serializers.FileUploadSerializer
    model = models.Attachment
    permission_classes = (IsApproved,)

    def get_queryset(self):
        return self.model.objects.all()

    def has_ownership(self, instance):
        return bool(self.request.user == instance.user)

    def perform_destroy(self, instance):
        tools.destroy_attachment(instance)


class AttachmentListViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.FileAttachedSerializer
    model = models.Attachment
    permission_classes = (IsApproved,)

    def get_queryset(self):
        app = self.kwargs[Const.QUERY_PARAM_APP]
        key = self.kwargs[Const.QUERY_PARAM_KEY]
        q = self.request.query_params.get(Const.QUERY_PARAM_SEARCH)
        return self.model.objects.attached(app, key, q)


class AttachmentManageViewSet(AttachmentListViewSet):
    serializer_class = serializers.FileSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        q = self.request.query_params.get(Const.QUERY_PARAM_SEARCH)
        return self.model.objects.search(q)
