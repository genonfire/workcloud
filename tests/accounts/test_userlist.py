from core.response import Response
from core.testcase import TestCase


class UserListTest(TestCase):
    def setUp(self):
        pass

    def test_get_users_permission(self):
        self.create_user()

        response = self.get(
            '/api/accounts/users/',
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.get(
            '/api/accounts/users/staff/',
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.get(
            '/api/accounts/users/',
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/accounts/users/staff/',
        )
        assert response.status_code == Response.HTTP_401

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
            assert (
                user.id == self.data[index].get('id') and
                user.username == self.data[index].get('username')
            )

        response = self.get(
            '/api/accounts/users/?q=bl',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2 and
            self.data[1].get('username') == 'black@color.com' and
            self.data[0].get('username') == 'blue@color.com'
        )

        self.get(
            '/api/accounts/users/staff/',
            auth=True
        )

        for index, staff in enumerate(reversed(staff_list)):
            assert (
                staff.id == self.data[index].get('id') and
                staff.username == self.data[index].get('username')
            )

        response = self.get(
            '/api/accounts/users/staff/?q=e',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2 and
            self.data[1].get('username') == 'white@color.com' and
            self.data[0].get('username') == 'purple@color.com'
        )
