from core.testcase import TestCase as CoreTestCase

from . import models


class TestCase(CoreTestCase):
    def create_option(
        self,
        is_active=True,
        permission_read='all',
        permission_write='all',
        permission_reply='all'
    ):
        self.option = models.Option.objects.create(
            is_active=True,
            permission_read=permission_read,
            permission_write=permission_write,
            permission_reply=permission_reply
        )
        return self.option

    def create_forum(
        self,
        name='illegallysmolcats',
        title='Illegally Small Cats',
        description='Why so small',
        option=None
    ):
        if not option:
            option = self.create_option()

        self.forum = models.Forum.objects.create(
            name=name,
            title=title,
            description=description,
            option=option
        )
        self.forum.managers.add(self.user)
        return self.forum
