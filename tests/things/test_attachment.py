from core.response import Response
from things.tests import TestCase


class FileUploadTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_attachment_upload_png(self):
        response = self.post(
            '/api/things/file/',
            {
                'file': self.png('image.png')
            },
            format='multipart',
            auth=True
        )

        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('content_type') == 'image/png' and
            self.data.get('size') == 58 and
            self.data.get('file') != 'image.png' and
            'image.png' in self.data.get('file')
        )

    def test_attachment_upload_same_file(self):
        self.post(
            '/api/things/file/',
            {
                'file': self.file()
            },
            format='multipart',
            auth=True
        )
        file = self.data

        response = self.post(
            '/api/things/file/',
            {
                'file': self.file()
            },
            format='multipart',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('file') != file.get('file') and
            self.data.get('content_type') == file.get('content_type') and
            self.data.get('size') == file.get('size')
        )

    def test_attachment_upload_invalid_param(self):
        response = self.post(
            '/api/things/file/',
            {
            },
            format='multipart',
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/things/file/',
            {
                'file': ''
            },
            format='multipart',
            auth=True
        )
        assert response.status_code == Response.HTTP_400

        response = self.post(
            '/api/things/file/',
            {
                'file': None
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_400

    def test_attachment_upload_max_size(self):
        data = 'R0lGODlhAQABAAD/ACwAAAAAAQABAAACAD'
        content = 'data:image/png;base64,' + data + data + data + 's='

        response = self.post(
            '/api/things/file/',
            {
                'file': self.png(content=content.encode('utf=8')),
            },
            format='multipart',
            auth=True
        )
        assert response.status_code == Response.HTTP_400


class FilePermissionTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_attachment()

    def test_attachment_manage_permission(self):
        response = self.get(
            '/api/things/files/',
            auth=True
        )
        assert response.status_code == Response.HTTP_403

    def test_attachment_delete_permission(self):
        self.post(
            '/api/things/file/',
            {
                'file': self.file()
            },
            format='multipart',
            auth=True
        )

        self.create_user(username='attacher@a.com')

        response = self.delete(
            '/api/things/file/%d/' % self.data.get('id'),
            auth=True
        )
        assert response.status_code == Response.HTTP_403


class FileManageTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_attachment()
        self.create_user(username='admin@a.com', is_staff=True)
        self.create_attachment(name='attachment.txt')

    def test_attachment_list_and_delete(self):
        response = self.get(
            '/api/things/files/?q=attachment',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            'attachment.txt' in self.data[0].get('file')
        )

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
