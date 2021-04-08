from core.response import Response
from communities.tests import TestCase


class ForumPermissionTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_forum_create_permission(self):
        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_403
        )

        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            format='json'
        )
        assert (
            response.status_code == Response.HTTP_401
        )


class ForumCreateTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_forum_null_name(self):
        response = self.post(
            '/api/communities/forum/',
            {
                'name': '',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/forum/',
            {
                'name': None,
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_forum_validate_fields(self):
        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/forum/',
            {
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'anonymous',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegally smolcats',
                'option': {
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats1',
                'option': {
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_201

        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats1',
                'option': {
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_forum_create_basic(self):
        response = self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )

        option = self.data.get('option')
        managers = self.data.get('managers')
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('name') == 'illegallysmolcats' and
            self.data.get('title') == 'Illegally Small Cats' and
            self.data.get('description') == 'why so small' and
            option.get('permission_read') == 'all' and
            option.get('permission_write') == 'staff' and
            option.get('permission_reply') == 'member' and
            managers[0].get('id') == self.user.id
        )


class ForumEditTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_edit_forum_option(self):
        response = self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'option': {
                    'permission_read': 'member',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )

        option = self.data.get('option')
        assert (
            response.status_code == Response.HTTP_200 and
            option.get('permission_read') == 'member' and
            option.get('permission_write') == 'staff' and
            option.get('permission_reply') == 'member' and
            option.get('is_active') == self.forum.is_active()
        )

    def test_edit_forum_managers(self):
        user = self.user
        self.create_user(
            username='111@a.com',
            is_staff=True
        )

        response = self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'managers': [
                    {
                        'id': user.id
                    },
                    {
                        'id': self.user.id
                    }
                ]
            },
            auth=True
        )

        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('managers')[0].get('id') == self.user.id and
            self.data.get('managers')[1].get('id') == user.id
        )

    def test_edit_forum_all_fields(self):
        response = self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'name': 'test',
                'title': 'test',
                'description': 'test',
                'option': {
                    'is_active': False,
                    'permission_read': 'member',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )

        option = self.data.get('option')
        assert (
            response.status_code == Response.HTTP_200 and
            option.get('permission_read') == 'member' and
            option.get('permission_write') == 'staff' and
            option.get('permission_reply') == 'member' and
            not option.get('is_active') and
            self.data.get('name') == self.forum.name and
            self.data.get('title') == 'test' and
            self.data.get('description') == 'test'
        )


class ForumDeleteTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_delete_forum(self):
        response = self.delete(
            '/api/communities/forum/%d/' % self.forum.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/communities/forums/%d/' % self.forum.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_404


class ForumListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_get_forums(self):
        sample_name = [
            'black',
            'white',
            'red',
            'blue',
            'purple',
        ]
        sample_title = [
            'tiger',
            'blackcat',
            'dragon',
            'fish',
            'snake',
        ]
        forum_list = []
        for index in range(5):
            forum = self.create_forum(
                name=sample_name[index],
                title=sample_title[index]
            )
            forum_list.append(forum)

        self.get(
            '/api/communities/forums/',
            auth=True
        )

        for index, forum in enumerate(reversed(forum_list)):
            assert (
                forum.id == self.data[index].get('id') and
                forum.name == self.data[index].get('name') and
                forum.title == self.data[index].get('title') and
                self.data[index].get('thread_count') == 0 and
                self.data[index].get('reply_count') == 0
            )

        response = self.get(
            '/api/communities/forums/?q=black',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            'black' in self.data[0].get('title') and
            'black' in self.data[1].get('name')
        )
