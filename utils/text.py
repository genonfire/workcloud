from django.utils.translation import gettext as _

from core.exceptions import BindError


class _Text(object):
    UNABLE_TO_LOGIN = _("Unable to login.")
    USER_IS_DEACTIVATED = _("User is deactivated.")
    INVALID_PASSWORD = _("Invalid password.")
    SAME_AS_OLD_PASSWORD = _("Same as old password.")

    def __setattr__(self, name, value):
        raise BindError("cannot re-bind text(%s)" % name)


Text = _Text()
