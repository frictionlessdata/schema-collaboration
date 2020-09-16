#!/bin/bash -e

python3 manage.py runserver 0.0.0.0:8000

#python3 manage.py migrate
#python3 manage.py collecstatic --no-input --clear
#
#gunicorn ProjectApplication.wsgi:application \
        #--bind 0.0.0.0:8085 \
        #--workers 3 \
        #--log-file=- \
        #--error-logfile=- \
        #--access-logfile=- \
        #--capture-output \
        #"$@"
