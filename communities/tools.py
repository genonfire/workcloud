from utils.debug import Debug  # noqa


def destroy_forum(instance):
    instance.option.delete()
    instance.delete()
