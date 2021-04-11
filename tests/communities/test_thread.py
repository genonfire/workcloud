from core.response import Response
from communities.tests import TestCase


class ThreadPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_permission_inactive_forum(self):
        option = self.create_option(is_active=False)
        self.create_forum(option=option)
        self.create_thread(forum=self.forum)

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert response.status_code == Response.HTTP_401

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test"'
            }
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test"'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': 'test patch',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403

    def test_permission_read_all_write_all(self):
        self.create_forum()

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert response.status_code == Response.HTTP_200

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'tester',
                'title': 'test',
                'content': 'test content',
            }
        )
        assert response.status_code == Response.HTTP_201

        thread_id = self.data.get('id')
        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id)
        )
        assert response.status_code == Response.HTTP_200

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            }
        )
        assert response.status_code == Response.HTTP_403

        response = self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id)
        )
        assert response.status_code == Response.HTTP_403

    def test_permission_read_all_write_member(self):
        option = self.create_option(permission_write='member')
        self.create_forum(option=option)
        self.create_user(username='ee@a.com')

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'tester',
                'title': 'test',
                'content': 'test content',
            }
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert response.status_code == Response.HTTP_200

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_201

        thread_id = self.data.get('id')
        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id)
        )
        assert response.status_code == Response.HTTP_200

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
        )
        assert response.status_code == Response.HTTP_401

        response = self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
        )
        assert response.status_code == Response.HTTP_401

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_200

    def test_permission_read_member_write_member(self):
        option = self.create_option(
            permission_read='member',
            permission_write='member'
        )
        self.create_forum(option=option)
        self.create_user(username='ee@a.com')

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert response.status_code == Response.HTTP_401

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'tester',
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_201

        thread_id = self.data.get('id')

        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id)
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_200

    def test_permission_read_staff_write_staff_by_member(self):
        option = self.create_option(
            permission_read='staff',
            permission_write='staff'
        )
        self.create_forum(option=option)

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_201

        thread_id = self.data.get('id')
        self.create_user(username='eee@a.com')

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403

    def test_permission_read_staff_write_staff_by_staff(self):
        option = self.create_option(
            permission_read='staff',
            permission_write='staff'
        )
        self.create_forum(option=option)

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_201

        thread_id = self.data.get('id')
        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_200

    def test_permission_trash(self):
        self.create_forum()
        self.create_user(username='m@a.com')

        response = self.get(
            '/api/communities/f/%s/trash/' % self.forum.name
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%s/trash/' % self.forum.name,
            auth=True
        )
        assert response.status_code == Response.HTTP_403


class ThreadModelTest(TestCase):
    def setUp(self):
        self.create_user(username='user@a.com', is_staff=True)
        self.create_forum()

    def test_thread_write_edit_delete(self):
        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('title') == 'test' and
            self.data.get('content') == 'content' and
            self.data.get('forum').get('id') == self.forum.id and
            self.data.get('user').get('username') == self.user.username
        )
        thread_id = self.data.get('id')

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'test2',
                'content': 'content2'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('title') == 'test2' and
            self.data.get('content') == 'content2' and
            self.data.get('forum').get('id') == self.forum.id and
            self.data.get('user').get('username') == self.user.username
        )

        response = self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('is_deleted')
        )

    def test_write_thread_with_user_or_name(self):
        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            not self.data.get('name') and
            self.data.get('user').get('username') == 'user@a.com'
        )

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'user',
                'title': 'test',
                'content': 'content'
            },
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('name') == 'user' and
            not self.data.get('user')
        )

    def test_thread_date_or_time(self):
        self.create_thread()

        response = self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )

        date_or_time = self.data.get('threads')[0].get('date_or_time')
        assert (
            response.status_code == Response.HTTP_200 and
            self.thread.date_or_time() == date_or_time
        )

    def test_thread_has_permission(self):
        self.create_user(username='2@a.com')
        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
            auth=True
        )
        thread_id = self.data.get('id')

        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert self.data.get('has_permission')

        self.create_user(username='3@a.com')
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert not self.data.get('has_permission')

        self.create_user(username='4@a.com', is_staff=True)
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        assert self.data.get('has_permission')

    def test_thread_pin_unpin(self):
        self.create_user(username='5@a.com')
        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content',
                'is_pinned': True
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            not self.data.get('is_pinned')
        )

        thread_id = self.data.get('id')

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'is_pinned': True
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('is_pinned')
        )

        response = self.post(
            '/api/communities/f/%s/%d/pin/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.post(
            '/api/communities/f/%s/%d/unpin/' % (self.forum.name, thread_id),
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        self.create_user(username='6@a.com', is_staff=True)

        response = self.post(
            '/api/communities/f/%s/%d/pin/' % (self.forum.name, thread_id),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('is_pinned')
        )

        response = self.post(
            '/api/communities/f/%s/%d/unpin/' % (self.forum.name, thread_id),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('is_pinned')
        )


class ThreadWriteException(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_write_thread_null(self):
        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': '',
                'content': 'content'
            },
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': None,
                'content': 'content'
            },
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': ''
            },
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': None
            },
        )
        assert response.status_code == Response.HTTP_400

    def test_edit_thread_null(self):
        self.create_thread()

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': '',
                'content': 'content2'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': None,
                'content': 'content2'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': 'test2',
                'content': ''
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': 'test2',
                'content': None
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400


class ThreadListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_thread_list(self):
        sample_title = [
            'black',
            'white',
            'red',
            'blue',
            'purple',
        ]
        sample_content = [
            'cat',
            'blacktiger',
            'dragon',
            'fish',
            'snake',
        ]
        thread_list = []
        for index in range(5):
            thread = self.create_thread(
                title=sample_title[index],
                content=sample_content[index]
            )
            thread_list.append(thread)

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )

        for index, thread in enumerate(reversed(thread_list)):
            assert (
                thread.id == self.data.get('threads')[index].get('id') and
                thread.title == self.data.get('threads')[index].get('title')
            )
        assert (
            self.data.get('forum').get('id') == self.forum.id and
            self.data.get('forum').get('name') == self.forum.name and
            self.data.get('forum').get('title') == self.forum.title
        )

        response = self.get(
            '/api/communities/f/%s/?q=black' % self.forum.name,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2 and
            self.data.get('threads')[1].get('title') == 'black' and
            self.data.get('threads')[0].get('title') == 'white'
        )

        trash = self.data.get('threads')[0]
        self.delete(
            '/api/communities/f/%s/%d/' % (
                self.forum.name,
                self.data.get('threads')[0].get('id')
            ),
            auth=True
        )
        self.get(
            '/api/communities/f/%s/?q=black' % self.forum.name,
            auth=True
        )
        assert (
            len(self.data.get('threads')) == 1 and
            self.data.get('threads')[0].get('title') == 'black'
        )

        response = self.get(
            '/api/communities/f/%s/trash/' % self.forum.name,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data.get('threads')) == 1 and
            self.data.get('threads')[0].get('title') == trash.get('title')
        )

        response = self.post(
            '/api/communities/f/%s/%d/restore/' % (
                self.forum.name, trash.get('id')
            ),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('id') == trash.get('id') and
            self.data.get('title') == trash.get('title') and
            not self.data.get('is_deleted')
        )


class ThreadPermissionFieldTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_permission_all(self):
        option = self.create_option(
            permission_write='all',
            permission_reply='all'
        )
        self.create_forum(option=option)
        self.create_thread()

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            )
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )

    def test_permission_member(self):
        option = self.create_option(
            permission_write='member',
            permission_reply='member'
        )
        self.create_forum(option=option)
        self.create_thread()

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert (
            not self.data.get('forum').get('permission_write') and
            not self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            )
        )
        assert (
            not self.data.get('forum').get('permission_write') and
            not self.data.get('forum').get('permission_reply')
        )

        self.create_user(username='member@a.com')
        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )

    def test_permission_staff(self):
        option = self.create_option(
            permission_write='staff',
            permission_reply='staff'
        )
        self.create_forum(option=option)
        self.create_thread()

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        assert (
            not self.data.get('forum').get('permission_write') and
            not self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            )
        )
        assert (
            not self.data.get('forum').get('permission_write') and
            not self.data.get('forum').get('permission_reply')
        )

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        assert (
            self.data.get('forum').get('permission_write') and
            self.data.get('forum').get('permission_reply')
        )

        self.create_user(username='member@a.com')
        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert (
            not self.data.get('forum').get('permission_write') and
            not self.data.get('forum').get('permission_reply')
        )
        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        assert (
            not self.data.get('forum').get('permission_write') and
            not self.data.get('forum').get('permission_reply')
        )


class ThreadPinTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()
        self.create_thread(title='pin me')

    def test_thread_pin_list(self):
        pin_thread = self.thread
        self.create_thread(title='stay me unpinned')

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert (
            self.data.get('threads')[1].get('title') == 'pin me' and
            self.data.get('threads')[0].get('title') == 'stay me unpinned'
        )

        self.post(
            '/api/communities/f/%s/%d/pin/' % (self.forum.name, pin_thread.id),
            auth=True
        )
        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        assert (
            self.data.get('threads')[0].get('title') == 'pin me' and
            self.data.get('threads')[1].get('title') == 'stay me unpinned'
        )
