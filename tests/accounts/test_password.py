from rest_framework.test import APIClient

from accounts import models
from core.response import Response
from core.testcase import TestCase


class PasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = 'p.king@a.com'
        self.password = 'password'
        self.first_name = 'Password'
        self.last_name = 'King'
        self.user = models.User.objects.create_user(
            username=self.username,
            email=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            is_approved=True
        )

        self.key = self.user.key()
        self.auth_header = 'Token ' + self.key
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        models.LoginDevice.objects.get_or_create(
            user=self.user,
            device='PC',
            os='Mac OS X',
            browser='Safari',
            ip_address='127.0.0.1'
        )

    def test_password_change(self):
        response = self.post(
            '/api/accounts/password_change/',
            {
                'old_password': self.password,
                'new_password': 'abcdefghijkl',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': 'abcdefghijkl'
            }
        )
        assert not self.data.get('key') == self.key

        self.auth_header = 'Token ' + self.data.get('key')
        response = self.get(
            '/api/accounts/devices/',
            auth=True
        )
        assert len(response.data.get('data')) == 1

    def test_password_change_check_wrong_password(self):
        response = self.post(
            '/api/accounts/password_change/',
            {
                'old_password': 'abcdefghijkl',
                'new_password': self.password,
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_password_change_check_same_password(self):
        response = self.post(
            '/api/accounts/password_change/',
            {
                'old_password': self.password,
                'new_password': self.password,
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_password_change_check_short_password(self):
        response = self.post(
            '/api/accounts/password_change/',
            {
                'old_password': self.password,
                'new_password': 'short',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400
