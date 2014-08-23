# !/usr/bin/env python
import os
import sys


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


from django.conf import settings

TEST_MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'media')

if not settings.configured:
    settings.configure(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'stdimage',
            'tests',
        ],
        ROOT_URLCONF='tests.urls',
        MEDIA_ROOT=TEST_MEDIA_ROOT,
        MEDIA_URL='/media/',
        STATIC_URL='/static/',
    )

if module_exists("django.test.runner.Discover"):
    from django.test.runner import DiscoverRunner as Runner
else:
    from django.test.simple import DjangoTestSuiteRunner as Runner


def runtests(*test_args):
    if not test_args:
        test_args = ['tests']
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)
    failures = Runner().run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
