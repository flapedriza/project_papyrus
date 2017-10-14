#!/usr/bin/env sh

set -u
set -e

./manage.py migrate --noinput
./manage.py collectstatic --noinput

if [ "${ENVIRON:-dev}" = "dev" ]
then
  ./manage.py runserver "0.0.0.0:8000"
else
  gunicorn -w 1 --log-level debug -b "0.0.0.0:8000" -t 60 wsgi:application
fi