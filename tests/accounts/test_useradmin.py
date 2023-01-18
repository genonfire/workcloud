from core.testcase import TestCase


class UserAdminBasicTest(TestCase):
    def setUp(self):
        self.user_a = self.create_user(username='a@a.com')
        self.user_b = self.create_user(username='b@a.com')
        self.create_user(is_staff=True, is_superuser=True)

    def test_user_admin_permission(self):
        self.patch(
            '/api/accounts/users/%d/' % self.user_a.id,
            {
                'call_name': 'A'
            }
        )
        self.status(401)

        self.delete(
            '/api/accounts/users/%d/' % self.user_b.id
        )
        self.status(401)

        self.create_user(username='c@a.com')

        self.patch(
            '/api/accounts/users/%d/' % self.user_b.id,
            {
                'call_name': 'B'
            },
            auth=True
        )
        self.status(403)

        self.delete(
            '/api/accounts/users/%d/' % self.user_a.id,
            auth=True
        )
        self.status(403)

    def test_user_admin_result(self):
        self.patch(
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
        self.status(200)
        self.check(self.data.get('first_name'), 'B')
        self.check(self.data.get('last_name'), 'Boy')
        self.check(self.data.get('call_name'), 'B-Boy')
        self.check(self.data.get('tel'), '+82 10 1234 5678')
        self.check(self.data.get('address'), '3245 146th PL SE')

        self.delete(
            '/api/accounts/users/%d/' % self.user_b.id,
            auth=True
        )
        self.status(200)

        self.get(
            '/api/accounts/users/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('first_name'), 'B')
        self.check(self.data[0].get('last_name'), 'Boy')
        self.check(self.data[0].get('call_name'), 'B-Boy')
        self.check(self.data[0].get('tel'), '+82 10 1234 5678')
        self.check(self.data[0].get('address'), '3245 146th PL SE')
