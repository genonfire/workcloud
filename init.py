import json
import os
import subprocess
import sys

from django.core.management.utils import get_random_secret_key


REPLACE_DIRS = [
    'accounts',
    'core',
    'utils',
    'workcloud',
    'tests',
    '.circleci',
]
REPLACE_FILES = [
    '.coveragerc',
    '.travis.yml',
    'manage.py',
    'README.md',
    'setup.py',
    'tox.ini',
]
IGNORE_FILES = [
    '.pyc',
]
SECRETS_PATH = 'secrets.json'
DEFAULT_SECRETS = {
    "DB_ENGINE": "django.db.backends.postgresql",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "",
    "DB_USER": "",
    "DB_PASSWORD": "",
    "EMAIL_HOST": "",
    "EMAIL_HOST_USER": "",
    "EMAIL_HOST_PASSWORD": "",
    "EMAIL_ADDRESS": "",
    "HOLIDAY_SERVICE_KEY": "",
    "SLACK_CHANNEL": "",
    "SLACK_TOKEN": "",
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
    "SECRET_KEY": get_random_secret_key()
}
CONFIG_PATH = 'config.json'
DEFAULT_CONFIG = {
    "DEBUG": True,
    "LOCAL_SERVER": True,
    "DEV_SERVER": False,
    "STAGING_SERVER": False,
    "TRACE_ENABLED": True,
    "DO_NOT_SEND_EMAIL": True
}


def rename_directory(project_name):
    os.rename('workcloud', project_name)


def replace_project(project_name):
    for filename in REPLACE_FILES:
        filepath = os.path.join('', filename)
        with open(filepath) as f:
            content = f.read()
        content = content.replace('workcloud', project_name)
        with open(filepath, 'w') as f:
            f.write(content)

    for replace_dir in REPLACE_DIRS:
        for dirname, dirs, files in os.walk(replace_dir):
            for filename in files:
                ignore = False
                for ignore_string in IGNORE_FILES:
                    if ignore_string in filename:
                        ignore = True
                        continue

                if not ignore:
                    filepath = os.path.join(dirname, filename)
                    with open(filepath) as f:
                        content = f.read()
                    content = content.replace('workcloud', project_name)
                    with open(filepath, 'w') as f:
                        f.write(content)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = os.path.split(os.getcwd())[1]
    replace_project(project_name)
    rename_directory(project_name)
    subprocess.call(['sh', './trans.sh'])

    if not os.path.isfile(SECRETS_PATH):
        with open(SECRETS_PATH, 'w') as f:
            f.write(json.dumps(DEFAULT_SECRETS, sort_keys=True, indent=4))

    if not os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            f.write(json.dumps(DEFAULT_CONFIG, sort_keys=True, indent=4))
