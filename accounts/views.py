from core.viewsets import (
    APIView,
    CreateAPIView,
    GenericAPIView,
    ModelViewSet
)
from core.permissions import (
    AllowAny,
    IsAdminUser,
    IsApproved,
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
    serializer_class = serializers.SignupSerializer
    permission_classes = (AllowAny,)


class UserLoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

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

    def get_response(self, user, login_device):
        data = {
            'key': login_device.user.key(),
            'user': user,
            'login_device': {
                'id': login_device.id,
                'device': login_device.device,
                'os': login_device.os,
                'browser': login_device.browser,
                'ip_address': login_device.ip_address,
                'is_registered': login_device.is_registered,
            },
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        self.request_log(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        user_serializer = self.set_serializer(serializers.IAmSerializer, user)
        login_device = self.login(request, user)

        return self.get_response(user_serializer.data, login_device)


class UserLogoutView(APIView):
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


class DeactivateAccountView(GenericAPIView):
    serializer_class = serializers.DeactivateAccountSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        models.LoginDevice.objects.filter(user=request.user).delete()
        tools.deactivate_account(request.user)

        return Response(status=Response.HTTP_200)


class LoginDeviceViewSet(ModelViewSet):
    serializer_class = serializers.LoginDeviceSerializer
    model = models.LoginDevice
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.none()

    def register(self, request, *args, **kwargs):
        instance = self.get_object()
        if tools.is_same_device(request, instance):
            tools.register_device(instance)
            return Response(status=Response.HTTP_200)
        else:
            return Response(status=Response.HTTP_400)


class PasswordChangeView(GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    sensitive_parameters = [
        'old_password',
        'new_password',
    ]


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    sensitive_parameters = [
        'new_password',
    ]


class UserSettingViewSet(ModelViewSet):
    serializer_class = serializers.UserSettingSerializer
    model = models.User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ConnectView(UserLoginView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_serializer = self.set_serializer(serializers.IAmSerializer, user)
        login_device = self.login(request, user)

        return self.get_response(user_serializer.data, login_device)


class UserListViewSet(ModelViewSet):
    serializer_class = serializers.UserInfoSerializer
    model = models.User
    permission_classes = (IsApproved,)

    def get_queryset(self):
        return self.model.objects.user_serach(self.q)


class StaffListViewSet(ModelViewSet):
    serializer_class = serializers.UsernameSerializer
    model = models.User
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.staff_search(self.q)


class UserAdminViewSet(ModelViewSet):
    serializer_class = serializers.UserSettingSerializer
    model = models.User
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.approved()

    def perform_delete(self, instance):
        models.LoginDevice.objects.filter(user=instance).delete()
        tools.deactivate_account(instance)
