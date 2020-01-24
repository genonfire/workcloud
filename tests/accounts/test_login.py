from core.response import Response
from core.testcase import TestCase


class LoginTest(TestCase):
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

    def test_login_check_useragent(self):
        self.client = self.get_client('PC')
        response = self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        assert response.status_code == Response.HTTP_200

        login_device = self.data.get('login_device')
        assert (
            login_device.get('device') == 'PC' and
            login_device.get('os') == 'Mac OS X' and
            login_device.get('browser') == 'Chrome'
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

    def test_login_check_inactive_user(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])

        response = self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        assert response.status_code == Response.HTTP_400
