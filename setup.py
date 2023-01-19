#!/usr/bin/env python3
import sys

from setuptools import find_packages, setup


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 8)


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name='workcloud',
    version=2.0,
    url='https://github.com/genonfire/workcloud',
    license='MIT',
    description='W.C. is workcloud',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='KJ Kim',
    author_email='gencode.me@gmail.com',
    packages=find_packages(exclude=['tests*', 'frontend', 'locale']),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.8",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={
        'Source': 'https://github.com/genonfire/workcloud',
    },
)
