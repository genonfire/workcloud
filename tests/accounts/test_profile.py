from django.core.files.uploadedfile import SimpleUploadedFile

from core.response import Response
from core.testcase import TestCase


class ProfileTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_connect(self):
        response = self.post(
            '/api/accounts/connect/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('key') == self.key and
            self.data.get('user').get('username') == self.user.username
        )

    def test_get_profile(self):
        response = self.get(
            '/api/accounts/setting/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('username') == self.user.username and
            self.data.get('first_name') == self.user.first_name and
            self.data.get('last_name') == self.user.last_name and
            self.data.get('call_name') == self.user.call_name and
            self.data.get('email') == self.user.email and
            self.data.get('is_approved') == self.user.is_approved
        )

    def test_update_profile(self):
        gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )
        photo = SimpleUploadedFile('photo.gif', gif, 'image/gif')
        response = self.patch(
            '/api/accounts/setting/',
            {
                'username': 'b-boy@b.com',
                'first_name': 'B',
                'last_name': 'Boy',
                'call_name': 'B-Boy',
                'photo': photo,
                'email': 'b-boy@b.com',
                'tel': '+82-10-1234-5678',
                'address': '3245 146th PL SE',
                'is_approved': not self.user.is_approved,
            },
            format='multipart',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('username') == self.user.username and
            self.data.get('first_name') == 'B' and
            self.data.get('last_name') == 'Boy' and
            self.data.get('call_name') == 'B-Boy' and
            self.data.get('email') == 'b-boy@b.com' and
            self.data.get('tel') == '+82-10-1234-5678' and
            self.data.get('address') == '3245 146th PL SE' and
            self.data.get('is_approved') == self.user.is_approved
        )

    def test_callname_not_allow_null(self):
        response = self.patch(
            '/api/accounts/setting/',
            {
                'first_name': 'B',
                'call_name': None,
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.patch(
            '/api/accounts/setting/',
            {
                'last_name': 'B',
                'call_name': '',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400
