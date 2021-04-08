from rest_framework.test import APIClient

from core.response import Response
from core.testcase import TestCase


class SignupTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = 'wc@workcloud-test.com'
        self.password = 'password'
        self.first_name = 'Work'
        self.last_name = 'Cloud'

    def test_signup_check_duplicate_username(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('username') == self.username and
            self.data.get('first_name') == self.first_name and
            self.data.get('last_name') == self.last_name
        )
        assert (
            self.data.get('call_name') == self.first_name + self.last_name or
            self.data.get('call_name') == self.last_name + self.first_name
        )

        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        assert response.status_code == Response.HTTP_400

    def test_signup_check_no_password(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        assert response.status_code == Response.HTTP_400

    def test_signup_check_no_first_name(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'last_name': self.last_name
            }
        )
        assert response.status_code == Response.HTTP_400

    def test_signup_check_no_last_name(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name
            }
        )
        assert response.status_code == Response.HTTP_400

    def test_signup_check_null_fields(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': None,
                'last_name': self.last_name
            }
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': '',
                'last_name': self.last_name
            }
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': None
            }
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': ''
            }
        )
        assert response.status_code == Response.HTTP_400
