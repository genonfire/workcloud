from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class SignupTests(TestCase):

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = 'wc@gencode.me'
        self.password = 'password'
        self.first_name = 'Work'
        self.last_name = 'Cloud'

    def test_signup_check_duplicate_username(self):
        response = self.client.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        response = self.client.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_signup_check_no_password(self):
        response = self.client.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_signup_check_no_first_name(self):
        response = self.client.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'last_name': self.last_name
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_signup_check_no_last_name(self):
        response = self.client.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
