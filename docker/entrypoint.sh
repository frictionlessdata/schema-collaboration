#!/bin/bash -e

python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

python3 manage.py check --deploy

python3 manage.py create_datamanagement_and_admin_user --only-if-no-people \
	"$DATAMANAGER_USERNAME" \
	"$DATAMANAGER_FULL_NAME" \
	"$DATAMANAGER_PASSWORD" \
	"$ADMIN_PASSWORD"

python3 manage.py create_default_data_package_status --only-if-no-status

/usr/bin/supervisord --configuration /etc/supervisor/conf.d/supervisord.conf
