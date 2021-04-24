from core.testcase import TestCase
from core.response import Response
from utils.text import Text


class I18NTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_i18n_prefix(self):
        response = self.post(
            '/en/api/accounts/login/',
            {
                'username': '1@a.com',
                'password': 'passworD'
            }
        )
        assert (
            response.status_code == Response.HTTP_400 and
            'Unable to login.' == response.data.get('non_field_errors')[0]
        )

    def test_i18n_default_no_prefix(self):
        response = self.post(
            '/api/accounts/login/',
            {
                'username': '1@a.com',
                'password': 'passworD'
            }
        )
        assert (
            response.status_code == Response.HTTP_400 and
            Text.UNABLE_TO_LOGIN == response.data.get('non_field_errors')[0]
        )
