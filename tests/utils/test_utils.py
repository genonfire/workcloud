from django.conf import settings

from core.exceptions import BindError
from core.testcase import TestCase
from utils.constants import Const
from utils.debug import Debug
from utils.text import Text


class UtilTest(TestCase):
    def test_set_const(self):
        result = False
        try:
            Const.NAME_MAX_LENGTH = 0
        except BindError:
            result = True
            self.log('Correctly raised BindError for Const.')

        try:
            Text.INVALID_TOKEN = 'Invalid Token'
        except BindError:
            result = True
            self.log('Correctly raised BindError for Text.')

        assert result

    def test_trace(self):
        result = False
        if Debug.test_mode():
            if not Debug._trace_enabled():
                settings.TRACE_ENABLED = True
            Debug.trace('Trace test.')
            Debug.error('Error test.')
            settings.TRACE_ENABLED = False
            result = True
        assert result

    def test_log(self):
        result = False
        if Debug.debug_or_test_mode():
            if not Debug.debug_mode():
                settings.DEBUG = True
            Debug.log('log test.')
            Debug.callstack(limit=0)
            settings.DEBUG = False
            result = True
        assert result
