from django.test import TestCase as _TestCase

from rest_framework.test import APIClient

from accounts.models import User
from accounts.tools import Test


class TestCase(_TestCase):
    def log(self, *args, **kwargs):
        print("#", *args, **kwargs)

    def get(self, path, data=None, auth=False, **extra):
        if auth:
            response = self.client.get(
                path, data, HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.get(path, data, **extra)

        self.data = response.data.get('data')
        return response

    def post(self, path, data=None, auth=False, **extra):
        if auth:
            response = self.client.post(
                path, data, HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.post(path, data, **extra)

        self.data = response.data.get('data')
        return response

    def put(self, path, data=None, auth=False, **extra):
        if auth:
            response = self.client.put(
                path, data, HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.put(path, data, **extra)

        self.data = response.data.get('data')
        return response

    def patch(self, path, data=None, auth=False, **extra):
        if auth:
            response = self.client.patch(
                path, data, HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.patch(path, data, **extra)

        self.data = response.data.get('data')
        return response

    def delete(self, path, data=None, auth=False, **extra):
        if auth:
            response = self.client.delete(
                path, data, HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.delete(path, data, **extra)

        self.data = response.data.get('data')
        return response

    def options(self, path, data=None, auth=False, **extra):
        if auth:
            response = self.client.options(
                path, data, HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.options(path, data, **extra)

        self.data = response.data.get('data')
        return response

    def create_user(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = Test.USERNAME
        self.password = Test.PASSWORD
        self.first_name = Test.FIRST_NAME
        self.last_name = Test.LAST_NAME
        self.user = User.objects.create_user(
            username=self.username,
            email=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            is_approved=True
        )

        self.key = self.user.key()
        self.auth_header = 'Token ' + self.key
