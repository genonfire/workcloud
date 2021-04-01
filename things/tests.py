from django.core.files.uploadedfile import SimpleUploadedFile

from core.testcase import TestCase as CoreTestCase

from . import models


class TestCase(CoreTestCase):
    def file(
        self,
        name='test.txt',
        content=b'test',
        content_type='text/plain'
    ):
        return SimpleUploadedFile(name, content, content_type)

    def png(
        self,
        name='image.png',
        content=b'data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=',
        content_type='image/png'
    ):
        return SimpleUploadedFile(name, content, content_type)

    def create_attachment(
        self,
        name='test.txt',
        content=b'test',
        content_type='text/plain',
        app='thread',
        key=1
    ):
        file = self.file(name, content, content_type)

        self.attachment = models.Attachment.objects.create(
            user=self.user,
            file=self.file(name, content, content_type),
            content_type=file.content_type,
            size=file.size,
            app=app,
            key=key
        )
        return self.attachment
