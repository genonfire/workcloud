from django.conf import settings

from utils.debug import Debug  # noqa


def _should_surname_ahead(language_code):
    languages_surname_ahead = [
        'ko-kr'
    ]

    if language_code in languages_surname_ahead:
        return True
    else:
        return False


def get_call_name(first_name, last_name, language_code=None):
    if not language_code:
        language_code = settings.LANGUAGE_CODE
    if _should_surname_ahead(language_code):
        call_name = '%s%s' % (last_name, first_name)
    else:
        call_name = '%s %s' % (first_name, last_name)

    return call_name
