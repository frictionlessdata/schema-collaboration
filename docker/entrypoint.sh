#!/bin/bash -e

echo "SECRET_KEY: $SECRET_KEY"

if [ x"$SECRET_KEY" == "x" ]
then
  export SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c60)
  echo "================================================================"
  echo "Warning: SECRET_KEY is empty. Please provide a Django secret key to keep the sessions valid between restarts"
  echo "A random SECRET_KEY has been generated. See this container's documentation or Django documentation for more information:"
  echo "https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY"
  echo "================================================================"
fi

if [ x"" == "" ]
then
  export ALLOWED_HOSTS="0.0.0.0"
  echo "================================================================"
  echo "Warning: ALLOWED_HOSTS was empty. Using 0.0.0.0 as a wildcard. Please see Django's documentation"
  echo "https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts"
  echo "You can use a list like 'localhost,schema-collaboration.yourisntitution.edu'"
  echo "================================================================"
fi

python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

python3 manage.py check --deploy

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

if [ x"$FORCE_SQLITE3_DATABASE" == "x1" ]
then
	echo "================================================================"
	echo "This instance is using sqlite3 database"
	echo "For production use a MariaDB server. Data might be lost"
	echo "unless you are using Docker volumes for the db.sqlite3 file"
	echo "================================================================"
fi

/usr/bin/supervisord --configuration /etc/supervisor/conf.d/supervisord.conf
