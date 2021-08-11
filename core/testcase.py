import accounts

from rest_framework.test import APIClient, APITestCase


class TestCase(APITestCase):
    def log(self, *args, **kwargs):
        print("#", *args, **kwargs)

    def get(self, path, data=None, format='json', auth=False, **extra):
        if auth:
            response = self.client.get(
                path, data, format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.get(path, data, format, **extra)

        self.data = response.data.get('data')
        return response

    def post(self, path, data=None, format='json', auth=False, **extra):
        if auth:
            response = self.client.post(
                path, data, format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.post(path, data, format, **extra)

        self.data = response.data.get('data')
        return response

    def put(self, path, data=None, format='json', auth=False, **extra):
        if auth:
            response = self.client.put(
                path, data, format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.put(path, data, format, **extra)

        self.data = response.data.get('data')
        return response

    def patch(self, path, data=None, format='json', auth=False, **extra):
        if auth:
            response = self.client.patch(
                path, data, format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.patch(path, data, format, **extra)

        self.data = response.data.get('data')
        return response

    def delete(self, path, data=None, format='json', auth=False, **extra):
        if auth:
            response = self.client.delete(
                path, data, format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.delete(path, data, format, **extra)

        self.data = response.data.get('data')
        return response

    def options(self, path, data=None, format='json', auth=False, **extra):
        if auth:
            response = self.client.options(
                path, data, format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.options(path, data, format, **extra)

        self.data = response.data.get('data')
        return response

    def get_client(self, device=None):
        if device == 'PC':
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'  # noqa
        else:
            user_agent = None

        return APIClient(enforce_csrf_checks=True, HTTP_USER_AGENT=user_agent)

    def create_user(
        self,
        username=None,
        is_staff=False,
        is_superuser=False,
    ):
        if not username:
            username = accounts.tools.Test.USERNAME

        self.username = username
        self.password = accounts.tools.Test.PASSWORD
        self.first_name = accounts.tools.Test.FIRST_NAME
        self.last_name = accounts.tools.Test.LAST_NAME
        self.call_name = accounts.tools.Test.CALL_NAME
        self.user = accounts.models.User.objects.create_user(
            username=self.username,
            email=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            call_name=self.call_name,
            is_approved=True,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        self.key = self.user.key()
        self.auth_header = 'Token ' + self.key
        return self.user
