from utils.debug import Debug  # noqa


def destroy_attachment(instance):
    if instance.file:
        instance.file.delete()
    instance.delete()
