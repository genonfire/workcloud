from core.response import Response
from core.testcase import TestCase


class LoginTests(TestCase):
    def setUp(self):
        self.create_user()

    def test_login_basic(self):
        response = self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        assert response.status_code == Response.HTTP_200
        assert self.data.get('key') == self.key

        login_device = self.data.get('login_device')
        assert (
            login_device.get('device') == 'Other' and
            login_device.get('os') == 'Other' and
            login_device.get('browser') == 'Other'
        )

    def test_login_check_wrong_username(self):
        response = self.post(
            '/api/accounts/login/',
            {
                'username': '2@a.com',
                'password': self.password
            }
        )
        assert response.status_code == Response.HTTP_400

    def test_login_check_wrong_password(self):
        response = self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': 'wrong_password'
            }
        )
        assert response.status_code == Response.HTTP_400
