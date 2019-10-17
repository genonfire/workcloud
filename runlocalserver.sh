#! /bin/bash
export DJANGO_DEBUG="Debug"
find . -name \*.pyc -delete
python manage.py runserver
