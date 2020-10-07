#!/bin/bash -e

if [ -z "$PORT" ]
then
  # This is passed to gunicorn via supervisord configuration file
  export PORT=8000
fi

if [ -z "$SECRET_KEY" ]
then
  export SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c60)
  echo "================================================================"
  echo "Warning: SECRET_KEY is empty. Please provide a Django secret key to keep the sessions valid between restarts"
  echo "A random SECRET_KEY has been generated. See this container's documentation or Django documentation for more information:"
  echo "https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY"
  echo "================================================================"
fi

if [ -z "$ALLOWED_HOSTS" ]
then
  export ALLOWED_HOSTS="*"
  echo "================================================================"
  echo "Warning: ALLOWED_HOSTS was empty. For now using * as a wildcard. Please see Django's documentation"
  echo "https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts"
  echo "You can use a list like 'localhost,schema-collaboration.yourinstitution.edu'"
  echo "If you use an invalid parameter you can see in the Docker output or the HTTP response what"
  echo "it should have been for your request"
  echo "================================================================"
fi

python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

if [ -n "$PRODUCTION_CHECKS" ] && [ "$PRODUCTION_CHECKS" == 1 ]
then
  echo "================================================================"
  python3 manage.py check --deploy
  echo "================================================================"
else
  echo "Skips production checks. Set PRODUCTION_CHECKS=1 to enable them"
fi

python3 manage.py create_datamanagement_and_admin_user --only-if-no-people \
	"$DATAMANAGER_USERNAME" \
	"$DATAMANAGER_FULL_NAME" \
	"$DATAMANAGER_PASSWORD" \
	"$ADMIN_PASSWORD"

# Unsets variables that are not used anymore
unset DATAMANAGER_USERNAME
unset DATAMANAGER_FULL_NAME
unset DATAMANAGER_PASSWORD
unset ADMIN_PASSWORD

python3 manage.py create_default_data_package_status --only-if-no-status

if [ -n "$FORCE_SQLITE3_DATABASE" ] && [ "$FORCE_SQLITE3_DATABASE" == "1" ]
then
	echo "================================================================"
	echo "This instance is using sqlite3 database"
	echo "For production use a MariaDB server. Data might be lost"
	echo "unless you are using Docker volumes for the db.sqlite3 file"
	echo "================================================================"
fi

/usr/bin/supervisord --configuration /etc/supervisor/conf.d/supervisord.conf
