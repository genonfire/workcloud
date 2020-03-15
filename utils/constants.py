from core.exceptions import BindError


class _Const(object):
    NAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128
    EMAIL_MAX_LENGTH = 254
    FILE_MAX_LENGTH = 128
    TEL_MAX_LENGTH = 100
    ADDRESS_MAX_LENGTH = 254
    IP_ADDRESS_MAX_LENGTH = 45
    DEFAULT_LINK_COUNT = 10

    def __setattr__(self, name, value):
        raise BindError("cannot re-bind const(%s)" % name)


Const = _Const()
