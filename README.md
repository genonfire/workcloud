# workcloud
[![API](https://github.com/genonfire/workcloud/actions/workflows/backend.yml/badge.svg?branch=master)](https://github.com/genonfire/workcloud/actions/workflows/backend.yml)
[![frontend](https://github.com/genonfire/workcloud/actions/workflows/frontend.yml/badge.svg?branch=master)](https://github.com/genonfire/workcloud/actions/workflows/frontend.yml)
[![codecov](https://codecov.io/gh/genonfire/workcloud/branch/master/graph/badge.svg)](https://codecov.io/gh/genonfire/workcloud)

Template for building web apps with Django REST framework + Vue.js


# Create database before setup

    $ psql
    postgres=# create user <DB_USER>;
    postgres=# alter user <DB_USER> with password '<DB_PASSWORD>';
    postgres=# create database <DB_NAME> owner <DB_USER>;


# Getting started with workcloud

    $ git clone https://github.com/genonfire/workcloud.git  # skip in case of template respository
    $ pip install -r requirements.txt
    $ cd frontend/wc
    $ npm install

- It is highly suggested to create your repository with workcloud template as below

![screenshot](docs/template_repository.png?raw=true "screenshot")


# Initialize project

    $ python init.py
    $ python manage.py migrate

- This will replace the name of 'workcloud' in all directories and contents of files to your project name
- This will create default secrets and config


# Local Server

    $ ./serve.sh
    $ cd frontend/wc
    $ npm run serve


# unittest

    $ tox  # You can use tox to generate coverage with unittest or just below script
    $ ./runtest.sh  # This has more options for convenience. check more with ./runtest.sh --help


# Swagger

    http://localhost:8000/redoc/
    http://localhost:8000/swagger/

- Available on localserver
