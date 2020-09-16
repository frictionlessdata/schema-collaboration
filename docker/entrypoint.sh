#!/bin/bash -e

python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

/usr/bin/supervisord --configuration /etc/supervisor/conf.d/supervisord.conf
