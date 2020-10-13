from core.exceptions import BindError


class _Const(object):
    """
    Common constants

    Reuseable constants as a boilerplate
    """

    NAME_MAX_LENGTH = 150
    KEY_MAX_LENGTH = 4
    PASSWORD_MAX_LENGTH = 128
    EMAIL_MAX_LENGTH = 254
    FILE_MAX_LENGTH = 128
    TEL_MAX_LENGTH = 100
    ADDRESS_MAX_LENGTH = 254
    IP_ADDRESS_MAX_LENGTH = 45
    DESC_MAX_LENGTH = 1024
    TITLE_MAX_LENGTH = 100
    DEFAULT_LINK_COUNT = 10

    def __setattr__(self, name, value):
        raise BindError("cannot re-bind const(%s)" % name)


class _ConstProject(_Const):
    """
    Project constants

    Just for this project
    """


Const = _ConstProject()
