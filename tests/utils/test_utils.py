from django.conf import settings

from core.testcase import TestCase
from utils.constants import Const
from utils.debug import Debug
from utils.text import Text
from utils.regexp import RegExpHelper


class UtilTest(TestCase):
    def test_set_const(self):
        result = False
        try:
            Const.NAME_MAX_LENGTH = 0
        except AttributeError:
            result = True

        try:
            Text.INVALID_TOKEN = 'Invalid Token'
        except AttributeError:
            result = True

        self.check(result)

    def test_print(self):
        result = False
        if Debug.test_mode():
            if not Debug._trace_enabled():
                settings.TRACE_ENABLED = True
            Debug.trace('\nTrace test.')
            Debug.error('Error test.')
            settings.TRACE_ENABLED = False
            result = True

        self.check(result)

        result = False
        if Debug.debug_or_test_mode():
            if not Debug.debug_mode():
                settings.DEBUG = True
            Debug.loooog('Log test.')
            Debug.callstack(limit=0)
            settings.DEBUG = False
            result = True

        self.check(result)

    def test_regexp(self):
        self.check(RegExpHelper.is_numbers('1234567890'))
        self.check_not(RegExpHelper.is_numbers('123-4567890'))
        self.check(RegExpHelper.numbers('010-1234-5678'), '01012345678')
        self.check_not(RegExpHelper.is_numbers(''))

        self.check(RegExpHelper.is_alphanumerics('abcdeFGHJKL9876'))
        self.check_not(RegExpHelper.is_alphanumerics('abcde@'))
        self.check_not(RegExpHelper.is_alphanumerics(''))
        self.check(RegExpHelper.alphanumerics('a@b.com'), 'abcom')

        self.check(RegExpHelper.is_uniwords('abc-123_Z'))
        self.check_not(RegExpHelper.is_uniwords('abc@'))
        self.check_not(RegExpHelper.is_uniwords(''))
