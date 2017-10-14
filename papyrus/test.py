from .settings import *

INSTALLED_APPS += [
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--ipdb',
    '--verbosity=3',
    '--logging-level=INFO',
]