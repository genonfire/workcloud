from core.testcase import TestCase


class UserListTest(TestCase):
    def setUp(self):
        pass

    def test_get_users_permission(self):
        self.create_user()

        self.get(
            '/api/accounts/users/',
            auth=True
        )
        self.status(200)

        self.get(
            '/api/accounts/users/staff/',
            auth=True
        )
        self.status(403)

        self.get(
            '/api/accounts/users/',
        )
        self.status(401)

        self.get(
            '/api/accounts/users/staff/',
        )
        self.status(401)

    def test_get_users(self):
        sample_name = [
            'black@color.com',
            'white@color.com',
            'red@color.com',
            'blue@color.com',
            'purple@color.com',
        ]
        sample_staff = [
            True,
            True,
            False,
            False,
            True,
        ]
        user_list = []
        staff_list = []

        for index in range(5):
            user = self.create_user(
                username=sample_name[index],
                is_staff=sample_staff[index]
            )
            user_list.append(user)

            if sample_staff[index]:
                staff_list.append(user)

        self.get(
            '/api/accounts/users/',
            auth=True
        )

        for index, user in enumerate(reversed(user_list)):
            self.check(user.id, self.data[index].get('id'))
            self.check(user.username, self.data[index].get('username'))

        self.get(
            '/api/accounts/users/?q=bl',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 2)
        self.check(self.data[1].get('username'), 'black@color.com')
        self.check(self.data[0].get('username'), 'blue@color.com')

        self.get(
            '/api/accounts/users/staff/',
            auth=True
        )
        for index, staff in enumerate(reversed(staff_list)):
            self.check(staff.id, self.data[index].get('id'))
            self.check(staff.username, self.data[index].get('username'))

        self.get(
            '/api/accounts/users/staff/?q=e',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 2)
        self.check(self.data[1].get('username'), 'white@color.com')
        self.check(self.data[0].get('username'), 'purple@color.com')
