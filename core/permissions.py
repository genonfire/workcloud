from rest_framework import permissions as rest_permission


class AllowAny(rest_permission.AllowAny):
    pass


class IsAuthenticated(rest_permission.IsAuthenticated):
    pass


class IsApproved(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_approved
        )


class IsAdminUser(rest_permission.IsAdminUser):
    pass
