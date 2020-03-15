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
        response = self.patch(
            '/api/accounts/setting/',
            {
                'username': 'b-boy@b.com',
                'first_name': 'B',
                'last_name': 'Boy',
                'call_name': 'B-Boy',
                'email': 'b-boy@b.com',
                'tel': '+82-10-1234-5678',
                'address': '3245 146th PL SE',
                'is_approved': not self.user.is_approved,
            },
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
