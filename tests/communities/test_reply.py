from core.response import Response
from communities.tests import TestCase


class ReplyPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_permission_reply_all(self):
        self.create_forum()
        self.create_thread()
        thread_id = self.thread.id

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            }
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('thread').get('id') == thread_id and
            self.data.get('reply_id') == 0 and
            not self.data.get('user') and
            self.data.get('name') == 'tester' and
            self.data.get('content') == 'test' and
            not self.data.get('is_deleted')
        )
        reply_id = self.data.get('id')

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            self.data[0].get('name') == 'tester' and
            self.data[0].get('content') == 'test'
        )

        response = self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit'
            },
        )
        assert response.status_code == Response.HTTP_401

        response = self.delete(
            '/api/communities/r/%d/' % reply_id
        )
        assert response.status_code == Response.HTTP_401

        response = self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        response = self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        self.create_user(username='2@a.com')

        response = self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_404

        response = self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_404

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('thread').get('id') == thread_id and
            self.data.get('reply_id') == 0 and
            self.data.get('user').get('id') == self.user.id and
            self.data.get('content') == 'test' and
            not self.data.get('is_deleted')
        )

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2
        )

    def test_permission_reply_member(self):
        option = self.create_option(
            permission_reply='member'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            }
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        assert response.status_code == Response.HTTP_200

        self.create_user(username='4@a.com')

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        reply_id = self.data.get('id')
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('content') == 'test' and
            self.data.get('user').get('username') == self.user.username
        )

        response = self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('content') == 'edit'
        )

        response = self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

    def test_permission_reply_staff(self):
        option = self.create_option(
            permission_reply='staff'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            }
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        assert response.status_code == Response.HTTP_200

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_201

        reply_id = self.data.get('id')

        response = self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('content') == 'edit'
        )

        response = self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        self.create_user(username='4@a.com')

        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_404

        response = self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_404

    def test_permission_thread_read_member(self):
        option = self.create_option(
            permission_read='member',
            permission_reply='member'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        self.create_user(username='2@a.com')
        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

    def test_permission_thread_read_staff(self):
        option = self.create_option(
            permission_read='staff',
            permission_reply='staff'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        assert response.status_code == Response.HTTP_401

        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        self.create_user(username='2@a.com')
        response = self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        assert response.status_code == Response.HTTP_403


class ReplyModelTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()
        self.create_thread()
        self.create_reply()

    def test_nested_reply(self):
        response = self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': 'test'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('reply_id') == 0
        )
        reply_id = self.data.get('id')

        response = self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': reply_id,
                'content': 'test'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('reply_id') == reply_id
        )

        response = self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': self.data.get('id'),
                'content': 'test'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('reply_id') == reply_id
        )

    def test_reply_edit_delete(self):
        response = self.patch(
            '/api/communities/r/%d/' % self.reply.id,
            {
                'content': 'bow wow'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('content') == 'bow wow' and
            self.data.get('reply_id') == 0 and
            not self.data.get('name')
        )

        response = self.patch(
            '/api/communities/r/%d/' % self.reply.id,
            {
                'reply_id': self.reply.id,
                'name': 'dog',
                'content': 'meow'
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('content') == 'meow' and
            self.data.get('reply_id') == 0 and
            not self.data.get('name')
        )

        response = self.delete(
            '/api/communities/r/%d/' % self.reply.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_200

        self.get(
            '/api/communities/f/%d/replies/' % self.thread.id,
            auth=True
        )
        assert (
            len(self.data) == 1 and
            self.data[0].get('is_deleted')
        )

    def test_reply_to_invalid_id(self):
        thread_id = int(self.thread.id) + 1
        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_404

        reply_id = int(self.reply.id) + 1
        response = self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'reply_id': reply_id,
                'content': 'test'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_404


class ReplyListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()
        self.create_thread()

    def test_reply_list(self):
        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': '1'
            },
            auth=True
        )
        reply_id = self.data.get('id')

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': '4'
            },
            auth=True
        )

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': reply_id,
                'content': '2'
            },
            auth=True
        )
        nested_reply_id = self.data.get('id')

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': '5'
            },
            auth=True
        )

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': nested_reply_id,
                'content': '3'
            },
            auth=True
        )

        self.get(
            '/api/communities/f/%d/replies/' % self.thread.id,
            auth=True
        )
        assert (
            len(self.data) == 5 and
            self.data[0].get('content') == '1' and
            self.data[0].get('reply_id') == 0 and
            self.data[1].get('content') == '2' and
            self.data[1].get('reply_id') == reply_id and
            self.data[2].get('content') == '3' and
            self.data[2].get('reply_id') == reply_id and
            self.data[3].get('content') == '4' and
            self.data[3].get('reply_id') == 0 and
            self.data[4].get('content') == '5' and
            self.data[4].get('reply_id') == 0
        )
