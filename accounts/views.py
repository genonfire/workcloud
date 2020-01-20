from core.viewsets import (
    CreateAPIView,
    GenericAPIView,
    ModelViewSet
)
from core.permissions import (
    AllowAny,
    IsAuthenticated
)
from core.response import Response
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
    tools
)


class UserSignupView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.SignupSerializer


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginSerializer

    def login(self, request, user):
        ip_address = tools.get_ip_address(request)
        device, os, browser = tools.get_user_agent(request)

        login_device, _ = models.LoginDevice.objects.get_or_create(
            user=user,
            device=device,
            os=os,
            browser=browser,
            ip_address=ip_address
        )

        tools.set_last_login(login_device)
        return login_device

    def get_response(self, login_device):
        data = {
            'key': login_device.user.key(),
            'login_device': {
                'id': login_device.id,
                'device': login_device.device,
                'os': login_device.os,
                'browser': login_device.browser,
                'ip_address': login_device.ip_address,
                'is_registered': login_device.is_registered
            }
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        login_device = self.login(request, user)

        return self.get_response(login_device)


class UserLogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        ip_address = tools.get_ip_address(request)
        device, os, browser = tools.get_user_agent(request)

        login_device = models.LoginDevice.objects.filter(
            user=request.user,
            device=device,
            os=os,
            browser=browser,
            ip_address=ip_address
        ).first()
        tools.delete_device(login_device)

        return Response(status=Response.HTTP_204)


class LoginDeviceViewSet(ModelViewSet):
    serializer_class = serializers.LoginDeviceSerializer
    model = models.LoginDevice

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def register(self, request, *args, **kwargs):
        instance = self.get_object()
        if tools.is_same_device(request, instance):
            tools.register_device(instance)
            return Response(status=Response.HTTP_200)
        else:
            return Response(status=Response.HTTP_400)
