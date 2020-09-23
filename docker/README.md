# schema-collaboration Docker

The Docker image created for this project can use an internal sqlite3 database (for testing). For production it requires a MariaDB/MySQL database.

## Start a `schema-collaboration` server instance
Download the image:
```
$ docker pull cpina/schema-collaboration
```

### Using a sqlite3 database
Execute it passing the environment variables to create the admin password and data manager user:
```
docker run \
    --interactive --tty \
    --name schema_collaboration \
    --publish 8000:80 \
    -e FORCE_SQLITE3_DATABASE=1 \
    -e ADMIN_PASSWORD=my_secret_pw \
    -e DATAMANAGER_USERNAME=data \
    -e DATAMANAGER_PASSWORD=dm_secret_pwd \
    -e DATAMANAGER_FULL_NAME="DataName DataSurname" \
    cpina/schema-collaboration
```

After running it:
 * Visit http://localhost:8000 to launch schema-collaboration
 * Visit http://localhost:8000/admin and login with User: admin Password: my_secret_pw
 * Visit http://localhost:8000/accounts/login/ and login with Username: data Password: dm_secret_pwd
 * Kill it with `Control+C`
 * Delete the image if you want to run again from scratch with `docker rm schema_collaboration`

**Warning:** above command uses sqlite3 database. This is meant for testing and evaluating. For production use please use a MariaDB/MySQL server.

### MariaDB database
For this you need to have a MariaDB/MySQL server with a user to access and manage the database. This user should have privileges to create and drop tables in the database. In case of doubt check your database manual. As a quick reference execute on the SQL shelL with enough privileges:
```
create database schema_collaboration;
use schema_collaboration;

-- to allow to connect from anywhere you can use '%', or the IP/hostname that the schema-collaboration will connect to.

create user 'schema_collaboration'@'%' identified by 'schema-collaboration-db-password';
grant all privileges on schema_collaboration.* to 'schema_collaboration'@'%';
flush privileges;
```

Then you can run `schema-collaboration` with the credentials for the database. E.g.:
```
docker run \
    --interactive \
    --name schema-collaboration \
    --publish 8000:80 \
    -e ADMIN_PASSWORD=my_secret_pw \
    -e DATAMANAGER_USERNAME=data \
    -e DATAMANAGER_PASSWORD=dm_secret_pwd \
    -e DATAMANAGER_FULL_NAME="DataName DataSurname" \
    -e DB_NAME=schema_collaboration \
    -e DB_USER=schema_collaboration \
    -e DB_PASSWORD=schema-collaboration-db-password \
    -e DB_HOST=localhost \
    -e DB_PORT=3306 \
    cpina/schema-collaboration
``` 

See the sqlite3 for the URLs.

## Via `docker-compose`

### sqlite3 example
Create a file named `docker-compose.yml` with the following content:
```
version: '3'

services:
  schema-collaboration:
    image: cpina/schema-collaboration
    environment:
      FORCE_SQLITE3_DATABASE: 1

      ADMIN_PASSWORD: admin_password
      DATAMANAGER_USERNAME: data
      DATAMANAGER_FULL_NAME: Data Manager
      DATAMANAGER_PASSWORD: secret_password
    ports:
      - "8000:80"
```

Execute:
```
$ docker-compose up --build
```

Visit http://localhost:8000

See sqlite3 section for the list of URLs to test.

### Generic example

An example file to be modified. See the "Environment variable in Compose" how to pass the variables: https://docs.docker.com/compose/environment-variables/

```
version: '3'

services:
  schema-collaboration:
    image: schema-collaboration
    environment:
      SECRET_KEY: ${SECRET_KEY}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS}
      FORCE_SQLITE3_DATABASE: ${FORCE_SQLITE3_DATABASE}

      # If FORCE_SQLITE3_DATABASE the next DB_ settings are not used
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_HOST: ${DB_HOST}
      DB_PORT: ${DB_PORT}

      ADMIN_PASSWORD: ${ADMIN_PASSWORD}
      DATAMANAGER_USERNAME: ${DATAMANAGER_USERNAME}
      DATAMANAGER_FULL_NAME: ${DATAMANAGER_FULL_NAME}
      DATAMANAGER_PASSWORD: ${DATAMANAGER_PASSWORD}
    ports:
      - "8000:80"
```

## Production deployment notes
When running the Docker schema-collaboration image it will execute the Django command `python3 manage.py check --deploy` and possibly show a list of warnings that can be addressed.

The schema-collaboration Docker image is designed to be easy to use for evaluating/testing but also ready to be used in production. This is the reason that is executing the Django deploy check and warnings are displayed. These warnings can be ignored if used for evaluating the image and should be fixed if used in production.

In certain circumstances depending on how the image is accessed some warnings might be not relevant. For example, the `SECURE_SSL_REDIRECT` might not be relevant this application is accessible only via `https`.

See the settings marked as *production* in the `Environment variables` section to help you to avoid warnings.

## Change other settings in `settings.py`
The most common settings to be changed can be configured just using environment variables.

You might need to tweak other settings in `settings.py`. If this is the case you can make a new At the end of the `settings.py` it includes `local_settings.py`. Make a file named `local_settings.py` available using a one file volume or building an Docker image to expose this file and any settings can be added or modified.

## Environment variables
Types of settings:
 * Django: direct mapping or almost direct mapping to Django settings. Includes link to the Django documentation
 * Optional: if not set the container will work (using defaults)
 * Production: relevant if deploying this container to production

### PRODUCTION_CHECKS (optional, production)
Set to 1 to enable the production checks.

This executes:
```
$ python3 manage.py checks --deploy
```

### `SECRET_KEY` (Django, optional, production)
If not provided it's generated every time that the container starts. Sessions, cookies, etc. will expire on every container run.

To generate it you could do on a Linux system:
```
$ tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c60
```

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key

### `ALLOWED_HOSTS` (Django, optional, production)
If not provided it uses the wildcard `*`.

List separated by commas for the `ALLOWED_HOSTS` Django setting.

Tip: if set to something invalid and `DEBUG=1` and try to use the application: a Django error will appear and will show what should be to handle the request.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts

### `DEBUG` (Django, optional, production)
Set to 0 to disable the debug outputs.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#debug

### `SECURE_SSL_REDIRECT` (Django, optional, production)
Set to `1` to redirect any http to https.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_SSL_REDIRECT

### `HSTS` (Django, optional, production)
Enables different Django settings at once:
 * `SECURE_HSTS_PRELOAD`. Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_HSTS_PRELOAD
 * `SECURE_HSTS_INCLUDE_SUBDOMAINS`. Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_HSTS_INCLUDE_SUBDOMAINS

### `SECURE_HSTS_SECONDS` (Django, optional, production)
Sets `SECURE_HSTS_SECONDS` in Django.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_HSTS_SECONDS

### `SECURE_PROXY_SSL_HEADER` (Django, optional, production)

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header

Tip: if you have infinite redirects from https to https or similar it might be because of this setting.

### `FORCE_SQLITE3_DATABASE` (optional)
If it's 1 it uses an SQLITE3 database: the container can be used without a MariaDB/MySQL database.

### `DB_HOST` (optional)
Specify the database host (or IP) to connect to. Only used if `FORCE_SQLITE3_DATABASE` is 0.

### `DB_PORT` (optional)
Specify the port of the database server. Defaults to 3306.

### `DB_NAME` (optional)
Specify the database name.

### `DB_USER` (optional)
Specify the database user.

### `DB_PASSWORD` (optional)
Specify the database password.

### `ADMIN_PASSWORD` (optional)
If initializing the database it creates an admin user with the given password.

### `DATAMANAGER_USERNAME` (optional)
If initializing the database it creates a datamanager username with the given username.

### `DATAMANAGER_PASSWORD`
If initializing the database it creates a datamanger password with the given password.

### `DATAMANAGER_FULL_NAME`
If initializing the database it creates a datamanager person with the given full name.
