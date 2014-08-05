#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, Command


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='django-stdimage',
    version='0.7.0',
    description='Django Standarized Image Field',
    author='codingjoe',
    url='https://github.com/codingjoe/django-stdimage',
    author_email='info@johanneshoppe.com',
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    packages=['stdimage'],
    include_package_data=True,
    requires=[
        'Django (>=1.5)',
        'Pillow (>=2.5)',
    ],
    install_requires=[
        'django>=1.5',
        'pillow>=2.5',
    ],
    cmdclass={'test': PyTest},
)
