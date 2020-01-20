from django.utils.translation import gettext as _

from core.exceptions import BindError


class _Text(object):
    UNABLE_TO_LOGIN = _("Unable to login.")
    USER_IS_DEACTIVATED = _("User is deactivated.")

    def __setattr__(self, name, value):
        raise BindError("cannot re-bind text(%s)" % name)


Text = _Text()
