
class _Const(object):
    """
    Common constants

    Reuseable constants as a boilerplate
    """

    KEY_MAX_LENGTH = 4
    FIELD_MAX_LENGTH = 20
    IP_ADDRESS_MAX_LENGTH = 45
    TEL_MAX_LENGTH = 100
    TITLE_MAX_LENGTH = 100
    PASSWORD_MAX_LENGTH = 128
    FILE_MAX_LENGTH = 128
    NAME_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254
    ADDRESS_MAX_LENGTH = 254
    DESC_MAX_LENGTH = 1024
    DIGITS_MAX_LENGTH = 12
    DECIMAL_PLACES_LENGTH = 6

    LENGTH_16 = 16
    LENGTH_32 = 32
    LENGTH_64 = 64
    LENGTH_128 = 128
    LENGTH_256 = 256
    LENGTH_512 = 512
    LENGTH_1024 = 1024

    DEFAULT_LINK_COUNT = 10
    QUERY_PARAM_SEARCH = 'q'
    QUERY_PARAM_PK = 'pk'
    QUERY_PARAM_FORUM = 'forum'

    TIME_FORMAT_DEFAULT = '%I:%M %p'

    MAX_REPLY_NESTING = 99
    PERMISSION_TYPE = ['all', 'member', 'staff']
    P_READ = 'read'
    P_WRITE = 'write'
    P_REPLY = 'reply'

    REQUIRED = {'required': True, 'allow_null': False, 'allow_blank': False}
    NOT_NULL = {'allow_null': False, 'allow_blank': False}

    def __setattr__(self, name, value):
        raise AttributeError("cannot re-bind const(%s)" % name)


class _ConstProject(_Const):
    """
    Project constants

    Just for this project
    """


Const = _ConstProject()
