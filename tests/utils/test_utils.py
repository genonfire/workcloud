from django.conf import settings

from core.exceptions import BindError
from core.testcase import TestCase
from utils.constants import Const
from utils.debug import Debug
from utils.text import Text


class UtilTest(TestCase):
    def test_set_const(self):
        try:
            Const.NAME_MAX_LENGTH = 0
            assert False
        except BindError:
            self.log('Correctly raised BindError for Const.')

        try:
            Text.INVALID_TOKEN = 'Invalid Token'
            assert False
        except BindError:
            self.log('Correctly raised BindError for Text.')

    def test_trace(self):
        if Debug.test_mode():
            if not Debug._trace_enabled():
                settings.TRACE_ENABLED = True
            Debug.trace('Trace test.')
            Debug.error('Error test.')
            settings.TRACE_ENABLED = False
        else:
            assert False

    def test_log(self):
        if Debug.debug_or_test_mode():
            if not Debug.debug_mode():
                settings.DEBUG = True
            Debug.log('log test.')
            Debug.callstack(limit=0)
            settings.DEBUG = False
        else:
            assert False
