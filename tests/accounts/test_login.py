from core.testcase import TestCase


class LoginTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_login_basic(self):
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.status(200)
        self.check(self.data.get('key'), self.key)

    def test_login_check_useragent(self):
        self.client = self.get_client('PC')
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.status(200)

        login_device = self.data.get('login_device')
        self.check(login_device.get('device'), 'PC')
        self.check(login_device.get('os'), 'Mac OS X')
        self.check(login_device.get('browser'), 'Chrome')

    def test_login_check_wrong_username(self):
        self.post(
            '/api/accounts/login/',
            {
                'username': '2@a.com',
                'password': self.password
            }
        )
        self.status(400)

    def test_login_check_wrong_password(self):
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': 'wrong_password'
            }
        )
        self.status(400)

    def test_login_check_inactive_user(self):
        self.post(
            '/api/accounts/deactivate/',
            {
                'consent': True,
            },
            auth=True
        )
        self.status(200)

        self.post(
            '/api/accounts/deactivate/',
            {
                'consent': True,
            },
            auth=True
        )
        self.status(401)

        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.status(400)

    def test_deactivate_user(self):
        self.post(
            '/api/accounts/deactivate/',
            {
                'consent': True,
            },
            auth=True
        )
        self.status(200)

        self.post(
            '/api/accounts/deactivate/',
            {
                'consent': True,
            },
            auth=True
        )
        self.status(401)

    def test_deactivate_user_no_consent(self):
        self.post(
            '/api/accounts/deactivate/',
            {
                'consent': False,
            },
            auth=True
        )
        self.status(400)
