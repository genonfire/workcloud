from core.exceptions import BindError


class _Const(object):

    def __setattr__(self, name, value):
        raise BindError("cannot re-bind const(%s)" % name)

    # Constants
    NAME_MAX_LENGTH = 150


Const = _Const()
