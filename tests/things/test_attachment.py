from core.response import Response

from things.tests import TestCase


class FileUploadTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_attachment_upload_png(self):
        response = self.post(
            '/api/things/file/upload/',
            {
                'file': self.png('image.png'),
                'app': 'thread',
                'key': 1,
            },
            auth=True
        )

        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('content_type') == 'image/png' and
            self.data.get('size') == 58 and
            self.data.get('app') == 'thread' and
            self.data.get('key') == 1 and
            self.data.get('file') != 'image.png' and
            'image.png' in self.data.get('file')
        )

    def test_attachment_upload_same_file(self):
        self.post(
            '/api/things/file/upload/',
            {
                'file': self.file(),
                'app': 'thread',
                'key': 1,
            },
            auth=True
        )
        file = self.data

        response = self.post(
            '/api/things/file/upload/',
            {
                'file': self.file(),
                'app': 'thread',
                'key': 1,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('file') != file.get('file') and
            self.data.get('content_type') == file.get('content_type') and
            self.data.get('size') == file.get('size') and
            self.data.get('app') == file.get('app') and
            self.data.get('key') == file.get('key')
        )

    def test_attachment_upload_invalid_param(self):
        response = self.post(
            '/api/things/file/upload/',
            {
                'app': 'thread',
                'key': 1,
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/things/file/upload/',
            {
                'file': self.file(),
                'app': 'thereisnoapplikethis',
                'key': 1,
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_attachment_upload_max_size(self):
        data = 'R0lGODlhAQABAAD/ACwAAAAAAQABAAACAD'
        content = 'data:image/png;base64,' + data + data + data + 's='

        response = self.post(
            '/api/things/file/upload/',
            {
                'file': self.png(content=content.encode('utf=8')),
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400


class FileListTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_attachment_manage_permission(self):
        response = self.get(
            '/api/things/files/',
            auth=True
        )
        assert response.status_code == Response.HTTP_403

    def test_attachment_list_invalid_params(self):
        self.create_attachment()
        response = self.get(
            '/api/things/files/thereisnoapplikethis/1/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not len(self.data)
        )

    def test_attachment_list_attached(self):
        self.create_attachment(
            name='test.pdf',
            content_type='application/pdf',
            content=b'pdf',
            app='thread',
            key=1
        )
        self.create_attachment(
            name='test.pdf',
            content_type='application/pdf',
            content=b'pdf',
            app='thread',
            key=1
        )
        self.create_attachment(
            name='test.pdf',
            content_type='application/pdf',
            content=b'pdf',
            app='thread',
            key=2
        )

        self.get(
            '/api/things/files/thread/1/',
            auth=True
        )
        assert len(self.data) == 2

        self.delete(
            '/api/things/file/%d/' % self.data[0].get('id'),
            auth=True
        )

        response = self.get(
            '/api/things/files/thread/1/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            self.data[0].get('content_type') == 'application/pdf' and
            self.data[0].get('size') == 3 and
            'test.pdf' in self.data[0].get('file')
        )


class FileManageTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_attachment()
        self.create_user(username='admin@a.com', is_staff=True)
        self.create_attachment()

    def test_attachment_list_and_delete(self):
        response = self.get(
            '/api/things/files/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2
        )

        response = self.delete(
            '/api/things/file/%d/' % self.data[1].get('id'),
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/things/files/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1
        )

        response = self.delete(
            '/api/things/file/%d/' % self.data[0].get('id'),
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/things/files/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 0
        )

    def test_attachment_attachment_permission(self):
        self.create_user(username='newbie@a.com')

        response = self.get(
            '/api/things/files/thread/1/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2
        )
        attachment_list = self.data

        response = self.delete(
            '/api/things/file/%d/' % attachment_list[1].get('id'),
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.delete(
            '/api/things/file/%d/' % attachment_list[0].get('id'),
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.get(
            '/api/things/files/thread/1/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2
        )
