from core.response import Response
from core.testcase import TestCase


class UserAdminBasicTest(TestCase):
    def setUp(self):
        self.user_a = self.create_user(username='a@a.com')
        self.user_b = self.create_user(username='b@a.com')
        self.create_user(is_staff=True, is_superuser=True)

    def test_user_admin_permission(self):
        response = self.patch(
            '/api/accounts/users/%d/' % self.user_a.id,
            {
                'call_name': 'A'
            }
        )
        assert response.status_code == Response.HTTP_401

        response = self.delete(
            '/api/accounts/users/%d/' % self.user_b.id
        )
        assert response.status_code == Response.HTTP_401

        self.create_user(username='c@a.com')

        response = self.patch(
            '/api/accounts/users/%d/' % self.user_b.id,
            {
                'call_name': 'B'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.delete(
            '/api/accounts/users/%d/' % self.user_a.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_403

    def test_user_admin_result(self):
        response = self.patch(
            '/api/accounts/users/%d/' % self.user_a.id,
            {
                "first_name": "B",
                "last_name": "Boy",
                "call_name": "B-Boy",
                "tel": "+82 10 1234 5678",
                "address": "3245 146th PL SE"
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('first_name') == 'B' and
            self.data.get('last_name') == 'Boy' and
            self.data.get('call_name') == 'B-Boy' and
            self.data.get('tel') == '+82 10 1234 5678' and
            self.data.get('address') == '3245 146th PL SE'
        )

        response = self.delete(
            '/api/accounts/users/%d/' % self.user_b.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.get(
            '/api/accounts/users/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            self.data[0].get('first_name') == 'B' and
            self.data[0].get('last_name') == 'Boy' and
            self.data[0].get('call_name') == 'B-Boy' and
            self.data[0].get('tel') == '+82 10 1234 5678' and
            self.data[0].get('address') == '3245 146th PL SE'
        )
