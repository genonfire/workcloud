from communities.tests import TestCase


class ThreadPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_permission_inactive_forum(self):
        option = self.create_option(is_active=False)
        self.create_forum(option=option)
        self.create_thread(forum=self.forum)

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        self.status(401)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test"'
            }
        )
        self.status(401)

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test"'
            },
            auth=True
        )
        self.status(403)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': 'test patch',
            },
            auth=True
        )
        self.status(403)

    def test_permission_read_all_write_all(self):
        self.create_forum()

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        self.status(200)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'tester',
                'title': 'test',
                'content': 'test content',
            }
        )
        self.status(201)

        thread_id = self.data.get('id')
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id)
        )
        self.status(200)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            }
        )
        self.status(403)

        self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id)
        )
        self.status(403)

    def test_permission_read_all_write_member(self):
        option = self.create_option(permission_write='member')
        self.create_forum(option=option)
        self.create_user(username='ee@a.com')

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'tester',
                'title': 'test',
                'content': 'test content',
            }
        )
        self.status(401)

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        self.status(200)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        self.status(201)

        thread_id = self.data.get('id')
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id)
        )
        self.status(200)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
        )
        self.status(401)

        self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
        )
        self.status(401)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)

    def test_permission_read_member_write_member(self):
        option = self.create_option(
            permission_read='member',
            permission_write='member'
        )
        self.create_forum(option=option)
        self.create_user(username='ee@a.com')

        self.get(
            '/api/communities/f/%s/' % self.forum.name
        )
        self.status(401)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'tester',
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        self.status(201)

        thread_id = self.data.get('id')
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id)
        )
        self.status(401)

        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)

    def test_permission_read_staff_write_staff_by_member(self):
        option = self.create_option(
            permission_read='staff',
            permission_write='staff'
        )
        self.create_forum(option=option)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        self.status(201)

        thread_id = self.data.get('id')
        self.create_user(username='eee@a.com')

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.status(403)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        self.status(403)

        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(403)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        self.status(403)

    def test_permission_read_staff_write_staff_by_staff(self):
        option = self.create_option(
            permission_read='staff',
            permission_write='staff'
        )
        self.create_forum(option=option)

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'test content',
            },
            auth=True
        )
        self.status(201)

        thread_id = self.data.get('id')
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'tested'
            },
            auth=True
        )
        self.status(200)

    def test_permission_trash(self):
        self.create_forum()
        self.create_user(username='m@a.com')

        self.get(
            '/api/communities/f/%s/trash/' % self.forum.name
        )
        self.status(401)

        self.get(
            '/api/communities/f/%s/trash/' % self.forum.name,
            auth=True
        )
        self.status(403)


class ThreadModelTest(TestCase):
    def setUp(self):
        self.create_user(username='user@a.com', is_staff=True)
        self.create_forum()

    def test_thread_write_edit_delete(self):
        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('title'), 'test')
        self.check(self.data.get('content'), 'content')
        self.check(self.data.get('forum').get('id'), self.forum.id)
        self.check(self.data.get('user').get('username'), self.user.username)

        thread_id = self.data.get('id')
        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'title': 'test2',
                'content': 'content2'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('title'), 'test2')
        self.check(self.data.get('content'), 'content2')
        self.check(self.data.get('forum').get('id'), self.forum.id)
        self.check(self.data.get('user').get('username'), self.user.username)

        self.delete(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)

        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)
        self.check(self.data.get('is_deleted'))

    def test_write_thread_with_user_or_name(self):
        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
        )
        self.status(400)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content'
            },
            auth=True
        )
        self.status(201)
        self.check_not(self.data.get('name'))
        self.check(self.data.get('user').get('username'), 'user@a.com')

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'name': 'user',
                'title': 'test',
                'content': 'content'
            },
        )
        self.status(201)
        self.check(self.data.get('name'), 'user')
        self.check_not(self.data.get('user'))

    def test_thread_date_or_time(self):
        self.create_thread()

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.status(200)

        self.check(
            self.data.get('threads')[0].get('date_or_time'),
            self.thread.date_or_time()
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
        self.check(self.data.get('has_permission'))

        self.create_user(username='3@a.com')
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.check_not(self.data.get('has_permission'))

        self.create_user(username='4@a.com', is_staff=True)
        self.get(
            '/api/communities/f/%s/read/%d/' % (self.forum.name, thread_id),
            auth=True
        )
        self.check(self.data.get('has_permission'))

    def test_thread_pin_unpin(self):
        self.create_user(username='5@a.com')
        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': 'content',
                'is_pinned': True
            },
            auth=True
        )
        self.status(201)
        self.check_not(self.data.get('is_pinned'))

        thread_id = self.data.get('id')
        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, thread_id),
            {
                'is_pinned': True
            },
            auth=True
        )
        self.status(200)
        self.check_not(self.data.get('is_pinned'))

        self.post(
            '/api/communities/f/%s/%d/pin/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(403)

        self.post(
            '/api/communities/f/%s/%d/unpin/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(403)

        self.create_user(username='6@a.com', is_staff=True)

        self.post(
            '/api/communities/f/%s/%d/pin/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)
        self.check(self.data.get('is_pinned'))

        self.post(
            '/api/communities/f/%s/%d/unpin/' % (self.forum.name, thread_id),
            auth=True
        )
        self.status(200)
        self.check_not(self.data.get('is_pinned'))


class ThreadWriteException(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_write_thread_null(self):
        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': '',
                'content': 'content'
            },
        )
        self.status(400)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': None,
                'content': 'content'
            },
        )
        self.status(400)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': ''
            },
        )
        self.status(400)

        self.post(
            '/api/communities/f/%s/write/' % self.forum.name,
            {
                'title': 'test',
                'content': None
            },
        )
        self.status(400)

    def test_edit_thread_null(self):
        self.create_thread()

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': '',
                'content': 'content2'
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': None,
                'content': 'content2'
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': 'test2',
                'content': ''
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/communities/f/%s/%d/' % (self.forum.name, self.thread.id),
            {
                'title': 'test2',
                'content': None
            },
            auth=True
        )
        self.status(400)


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
            self.check(self.data.get('threads')[index].get('id'), thread.id)
            self.check(
                self.data.get('threads')[index].get('title'),
                thread.title
            )

        self.check(self.data.get('forum').get('id'), self.forum.id)
        self.check(self.data.get('forum').get('name'), self.forum.name)
        self.check(self.data.get('forum').get('title'), self.forum.title)

        self.get(
            '/api/communities/f/%s/?q=black' % self.forum.name,
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 2)
        self.check(self.data.get('threads')[1].get('title'), 'black')
        self.check(self.data.get('threads')[0].get('title'), 'white')

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
        self.check(len(self.data.get('threads')), 1)
        self.check(self.data.get('threads')[0].get('title'), 'black')

        self.get(
            '/api/communities/f/%s/trash/' % self.forum.name,
            auth=True
        )
        self.status(200)
        self.check(len(self.data.get('threads')), 1)
        self.check(
            self.data.get('threads')[0].get('title'),
            trash.get('title')
        )

        self.post(
            '/api/communities/f/%s/%d/restore/' % (
                self.forum.name, trash.get('id')
            ),
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), trash.get('id'))
        self.check(self.data.get('title'), trash.get('title'))
        self.check_not(self.data.get('is_deleted'))


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
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            )
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

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
        self.check_not(self.data.get('forum').get('permission_write'))
        self.check_not(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            )
        )
        self.check_not(self.data.get('forum').get('permission_write'))
        self.check_not(self.data.get('forum').get('permission_reply'))

        self.create_user(username='member@a.com')
        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

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
        self.check_not(self.data.get('forum').get('permission_write'))
        self.check_not(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            )
        )
        self.check_not(self.data.get('forum').get('permission_write'))
        self.check_not(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        self.check(self.data.get('forum').get('permission_write'))
        self.check(self.data.get('forum').get('permission_reply'))

        self.create_user(username='member@a.com')
        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.check_not(self.data.get('forum').get('permission_write'))
        self.check_not(self.data.get('forum').get('permission_reply'))

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        self.check_not(self.data.get('forum').get('permission_write'))
        self.check_not(self.data.get('forum').get('permission_reply'))


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
        self.check(self.data.get('threads')[1].get('title'), 'pin me')
        self.check(
            self.data.get('threads')[0].get('title'),
            'stay me unpinned'
        )

        self.post(
            '/api/communities/f/%s/%d/pin/' % (self.forum.name, pin_thread.id),
            auth=True
        )
        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.check(self.data.get('threads')[0].get('title'), 'pin me')
        self.check(
            self.data.get('threads')[1].get('title'),
            'stay me unpinned'
        )
