from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    IsAdminUser,
    IsApproved,
)
from core.response import Response

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


class AttachmentManageViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.FileSerializer
    model = models.Attachment
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.search(self.q)


class HolidayViewSet(ModelViewSet):
    serializer_class = serializers.HolidaySerializer
    model = models.Holiday
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.all()


class HolidayYearViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.HolidaySerializer
    model = models.Holiday
    permission_classes = (IsApproved,)

    def get_queryset(self):
        return self.model.objects.year(self.kwargs['year'])

    def update(self, request, *args, **kwargs):
        data = tools.update_holiday(
            self.kwargs['year'],
            self.serializer_class
        )
        return Response(data, status=Response.HTTP_200)
