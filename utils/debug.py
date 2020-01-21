import logging
import traceback

from django.conf import settings


logger = logging.getLogger('workcloud.trace')


class _Debug:

    def debug_mode(self):
        if settings.DEBUG:
            return True
        else:
            return False

    def test_mode(self):
        if settings.TEST_SETTING:
            return True
        else:
            return False

    def debug_or_test_mode(self):
        if settings.DEBUG or settings.TEST_SETTING:
            return True
        else:
            return False

    def _trace_enabled(self):
        if settings.TRACE_ENABLED:
            return True
        else:
            return False

    def _log_enabled(self):
        return self.debug_mode()

    def trace(self, *args, **kwargs):
        if self._trace_enabled():
            logger.info(*args, **kwargs)

    def log(self, *args, **kwargs):
        if self._log_enabled():
            print("#", *args, **kwargs)

    def callstack(self, *args, **kwargs):
        if self.debug_mode():
            traceback.print_stack()


Debug = _Debug()
