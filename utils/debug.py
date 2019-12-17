import traceback

from django.conf import settings


class Debug:

    @classmethod
    def _debug_mode(cls):
        if settings.DEBUG:
            return True
        else:
            return False

    @classmethod
    def _trace_enabled(cls):
        if settings.TRACE_ENABLED:
            return True
        else:
            return False

    @classmethod
    def _log_enabled(cls):
        return cls._debug_mode()

    @classmethod
    def trace(cls, event, *args, **kwargs):
        if cls._trace_enabled():
            print("[%s]" % event, *args, **kwargs)

    @classmethod
    def log(cls, *args, **kwargs):
        if cls._log_enabled():
            print("#", *args, **kwargs)

    @classmethod
    def callstack(cls, *args, **kwargs):
        if cls._debug_mode():
            traceback.print_stack()
