import logging
import traceback

from django.conf import settings


logger = logging.getLogger('workcloud.trace')


class _Debug:

    def debug_mode(self):
        return settings.DEBUG

    def test_mode(self):
        return settings.TEST_SETTING

    def debug_or_test_mode(self):
        return bool(settings.DEBUG or settings.TEST_SETTING)

    def _trace_enabled(self):
        return settings.TRACE_ENABLED

    def _log_enabled(self):
        return self.debug_mode()

    def trace(self, *args, **kwargs):
        if self._trace_enabled():
            logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self._trace_enabled():
            logger.error(*args, **kwargs)

    def log(self, *args, **kwargs):
        if self._log_enabled():
            print("#", *args, **kwargs)

    def callstack(self, *args, **kwargs):
        if self.debug_mode():
            traceback.print_stack(*args, **kwargs)


Debug = _Debug()
