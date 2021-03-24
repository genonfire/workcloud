import os
import subprocess
import sys


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
                        print(filepath)
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
