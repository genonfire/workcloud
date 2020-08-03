from django.utils.translation import gettext as _

from core.exceptions import BindError


class _Text(object):
    """
    Common text

    Reuseable text as a boilerplate
    """

    UNABLE_TO_LOGIN = _("Unable to login.")
    USER_IS_DEACTIVATED = _("User is deactivated.")
    INVALID_PASSWORD = _("Invalid password.")
    SAME_AS_OLD_PASSWORD = _("Same as old password.")
    USER_NOT_EXIST = _("User not exist.")
    INVALID_UID = _("Invalid uid.")
    INVALID_TOKEN = _("Invalid token.")
    YOU_MUST_CONSENT = _("You must consent.")

    def __setattr__(self, name, value):
        raise BindError("cannot re-bind text(%s)" % name)


class _TextProject(_Text):
    """
    Project text

    Just for this project
    """


Text = _TextProject()
