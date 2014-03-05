#!/bin/sh
# This script makes sure that Jenkins can properly run your tests against your
# codebase.
set -e

DB_HOST="localhost"
DB_USER="hudson"

cd $WORKSPACE
VENV=$WORKSPACE/venv

echo "Starting build on executor $EXECUTOR_NUMBER..."

# Make sure there's no old pyc files around.
find . -name '*.pyc' -exec rm {} \;

if [ ! -d "$VENV/bin" ]; then
  echo "No virtualenv found.  Making one..."
  virtualenv $VENV --no-site-packages
  source $VENV/bin/activate
  pip install --upgrade pip
  pip install coverage
fi

git submodule update --init --recursive

if [ ! -d "$WORKSPACE/vendor" ]; then
    echo "No /vendor... crap."
    exit 1
fi

source $VENV/bin/activate
pip install -q -r requirements/compiled.txt
pip install -q -r requirements/dev.txt

cat > affiliates/settings/local.py <<SETTINGS
from . import base

# Database name has to be set because of sphinx
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '${DB_HOST}',
        'NAME': '${JOB_NAME}',
        'USER': 'hudson',
        'PASSWORD': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=InnoDB',
            'charset' : 'utf8',
            'use_unicode' : True,
        },
        'TEST_NAME': 'test_${JOB_NAME}',
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

CELERY_ALWAYS_EAGER = True
BANNERS_HASH = (
    '299839978f965e3b17d926572f91b4fbc340896c',
    '5f5e8cc58fac3f658fca66be259590ea42963aa8',
)

SECRET_KEY = 'v9h9h09hg04gb984bgbfb4f09f'
HMAC_KEYS = {
    '2012-06-06': 'some secret',
}

from django_sha2 import get_password_hashers
PASSWORD_HASHERS = get_password_hashers(base.BASE_PASSWORD_HASHERS, HMAC_KEYS)

SESSION_COOKIE_SECURE = True

FACEBOOK_APP_ID = '00000000000'
FACEBOOK_APP_SECRET = '9906bc9a6bf96b9f0abaefe97f97e'
FACEBOOK_APP_NAMESPACE = 'jenkinstest'

SETTINGS

echo "Creating database if we need it..."
echo "CREATE DATABASE IF NOT EXISTS ${JOB_NAME}"|mysql -u $DB_USER -h $DB_HOST

echo "Starting tests..."
export FORCE_DB=1
coverage run manage.py test --noinput
coverage xml $(find apps lib -name '*.py')

echo "FIN"
