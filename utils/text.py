from django.utils import translation
from django.utils.translation import gettext_lazy as _


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
    USERNAME_EXISTS = _("Username exists.")
    INVALID_UID = _("Invalid uid.")
    INVALID_TOKEN = _("Invalid token.")
    YOU_MUST_CONSENT = _("You must consent.")

    INVALID_PERMISSION_TYPE = _("Invalid permission type")
    ALPHABETS_NUMBER_ONLY = _("alphabets and number only")

    REQUIRED_FIELD = _("This field is required.")
    INVALID_VALUE = _("Invalid value")
    FILE_TOO_LARGE = _("File too large")
    ALREADY_EXISTS = _("Already exists.")

    def __setattr__(self, name, value):
        raise AttributeError("cannot re-bind text(%s)" % name)

    def language(self):
        return translation.get_language()

    def activate(self, language=None):
        if not language:
            language = self.language()
        return translation.activate(language)


class _TextProject(_Text):
    """
    Project text

    Just for this project
    """


Text = _TextProject()
