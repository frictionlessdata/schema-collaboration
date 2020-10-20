# schema-collaboration Docker

Pre-requisite: Docker running in the system. See Docker documentation to install it (https://docs.docker.com/get-docker/) and optionally but recommended docker-compose (https://docs.docker.com/get-docker/). schema-collaboration can be used without Docker, please refer to the main README.md file.

This guide will help you set up schema-collaboration on your own desktop machine for testing or your server if you wish.
 
The Docker image created for this project can use an internal sqlite3 database or a MariaDB/MySQL.

The schema-collaboration Docker image can use an sqlite3 database (requires no setup) or can use a MariaDB/MySQL server (requires an existing server, not bundled with schema-collaboration Docker image). In addition you can choose to use `docker run` commands (see section `Using plain Docker commands`) or create a `docker-compose.yml` (see section `Using docker-compose`).

## Using plain Docker commands
Download the Docker image:
```
$ docker pull cpina/schema-collaboration
```

### Using an sqlite3 database
**Warning: if you intend to persist the data of this Docker container see the section `docker-compose` in order to setup the Docker volume. On destroying the container run in this example the database will be destroyed.**

Run the Docker image, passing the environment variables to create the admin password and data manager credentials:
```sh
$ docker run \
    --interactive --tty \
    --name schema_collaboration \
    --publish 8000:80 \
    -e FORCE_SQLITE3_DATABASE=1 \
    -e ADMIN_PASSWORD=admin_secret_pwd \
    -e DATAMANAGER_USERNAME=data \
    -e DATAMANAGER_PASSWORD=dm_secret_pwd \
    -e DATAMANAGER_FULL_NAME="DataName DataSurname" \
    cpina/schema-collaboration
```

When the Docker container is running you can:
 * Visit http://localhost:8000 to open schema-collaboration
 * Visit http://localhost:8000/admin and login with User: admin Password: admin_secret_pwd
 * Visit http://localhost:8000/accounts/login/ and login with Username: data Password: dm_secret_pwd

If you want to run it again from scratch delete the container: `docker rm schema_collaboration` **This deletes the database**

### MariaDB database
For this you need to have a MariaDB/MySQL server with a user to access and manage the database. This user should have privileges to create and drop tables in the database.

With sufficient privileges, execute the following in an SQL shell:
```sql
create database schema_collaboration;
use schema_collaboration;

-- to allow to connect from anywhere you can use '%', or the IP/hostname that the schema-collaboration will connect to.

create user 'schema_collaboration'@'%' identified by 'schema-collaboration-db-password';
grant all privileges on schema_collaboration.* to 'schema_collaboration'@'%';
flush privileges;
```

Then you can run `schema-collaboration` with the credentials for the database. E.g.:
```sh
$ docker run \
    --interactive \
    --name schema-collaboration \
    --publish 8000:80 \
    -e ADMIN_PASSWORD=admin_secret_pwd \
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

See the sqlite3 for the URLs to use.

## Using `docker-compose`

### sqlite3 example
Create a file named `docker-compose.yml` with the following content:
```
version: '3'

services:
  schema-collaboration:
    image: cpina/schema-collaboration
    environment:
      FORCE_SQLITE3_DATABASE: 1

      ADMIN_PASSWORD: admin_secret_pwd
      DATAMANAGER_USERNAME: data
      DATAMANAGER_FULL_NAME: Data Manager
      DATAMANAGER_PASSWORD: dm_secret_pwd
    ports:
      - "8000:80"
    volumes:
      - /home/admin/schema-collaboration-data:/code/SchemaCollaboration/data
```

Execute:
```sh
$ docker-compose up --build
```

Visit http://localhost:8000. See other URLs in the first docker example.

### Generic example

An example file to be modified. See the section "Environment variable in Compose" in the documentation for how to pass the variables into `docker-compose`: https://docs.docker.com/compose/environment-variables/

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

      PRODUCTION_CHECKS: ${PRODUCTION_CHECKS}
    ports:
      - "8000:80"
```

## Production deployment notes
Set `PRODUCTION_CHECKS` to 1 in order to run the Django command `python3 manage.py check --deploy` . This might show warnings that you can fix using other variables depending on the configuration of your server. For example, the `SECURE_SSL_REDIRECT` might not be relevant if the application is accessible only via `https`.

See the settings marked as *production* in the `Environment variables` section to help you to fix the warnings.

## Change other settings in `settings.py`
Most common settings can be changed using environment variables.

You might need to tweak other settings in `settings.py`. If this is the case create a Docker image based on the current one and create a `local_settings.py` file. This file will be imported after `settings.py` so any variables can be created or overriden.

For example: create a new directory:
```sh
mkdir schema-collaboration-local-settings
```
And within this directory create a `local_settings.py` file which will contain any settings you wish to change. For example:
```
TIME_ZONE = 'Europe/Paris'
SECURE_REFERRER_POLICY = 'no-referrer'
```

Also create a file named `Dockerfile` within the same directory. This file should contain:
```
FROM cpina/schema-collaboration
COPY local_settings.py /code/SchemaCollaboration
```

Build the new image (using the new `schema-collaboration-local-settings`):
```sh
$ docker build -t schema-collaboration-local-settings .
```

Run the Docker image using the examples from above according to your database setup. Ensure you use the newly created image `schema-collaboration-local-settings:latest`, for example:
```sh
$ docker run -it -e FORCE_SQLITE3_DATABASE=1 --publish 8000:80 schema-collaboration-local-settings:latest
```


## Environment variables

The following environment variables are supported within the schema-collaboration Docker image. They can be changed within the docker-compose file or via the docker -e option. Their use is described below: 

Types of settings:
 * Django: direct mapping or almost direct mapping to Django settings. Includes link to the Django documentation
 * Production: relevant only if deploying this container to production

### PRODUCTION_CHECKS (production)
Set to 1 to enable the production checks.

This executes:
```sh
$ python3 manage.py checks --deploy
```

Provides Django warnings relevant only when deploying for production.

### `SECRET_KEY` (Django, production)
If not provided the secret key is generated every time that the container starts. Sessions, cookies, etc. will expire on every container run.

To generate it you could do on a Linux system:
```sh
$ tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c60
```

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key

### `ALLOWED_HOSTS` (Django, production)
If not provided it uses the wildcard `*`.

List separated by commas for the `ALLOWED_HOSTS` Django setting.

Tip: if set to something invalid and `DEBUG=1` when you try to use the applicatio, a Django error will appear and will show what this environment variable should contain to handle the request.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts

### `DEBUG` (Django, production)
Set to 0 to disable the debug outputs.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#debug

### `SECURE_SSL_REDIRECT` (Django, production)
Set to `1` to redirect http requests to https.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_SSL_REDIRECT

If this is set to 1 there are two other settings that are set to True:
 * CSRF_COOKIE_SECURE: https://docs.djangoproject.com/en/3.1/ref/settings/#csrf-cookie-secure
 * SESSION_COOKIE_SECURE: https://docs.djangoproject.com/en/3.1/ref/settings/#session-cookie-secure

### `HSTS` (Django, production)
Set to `1` to enable the following Django settings to True:
 * `SECURE_HSTS_PRELOAD`. Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_HSTS_PRELOAD
 * `SECURE_HSTS_INCLUDE_SUBDOMAINS`. Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_HSTS_INCLUDE_SUBDOMAINS

### `SECURE_HSTS_SECONDS` (Django, production)
Set it to a number of seconds and it is set to the `SECURE_HSTS_SECONDS` in Django.

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECURE_HSTS_SECONDS

### `SECURE_PROXY_SSL_HEADER` (Django, production)

Django documentation: https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header

Tip: if you have infinite redirects from http to https or similar it might be because of this setting.

### `FORCE_SQLITE3_DATABASE`
If this setting is `1` schema-collaboration uses an sqlite3 database: the container can be used without a MariaDB/MySQL server.

### `DB_HOST`
Used only if using MariaDB/Mysql server.

Specify the database host (or IP) to connect to. Only used if `FORCE_SQLITE3_DATABASE` is 0.

### `DB_PORT`
Used only if using MariaDB/Mysql server.

Specify the port of the database server. Defaults to 3306.

### `DB_NAME`
Used only if using MariaDB/Mysql server.

Specify the database name.

### `DB_USER`
Used only if using MariaDB/Mysql server.

Specify the database user.

### `DB_PASSWORD`
Used only if using MariaDB/Mysql server.

Specify the database password.

### `ADMIN_PASSWORD`
If initializing the database it creates an admin user with the given password.

### `DATAMANAGER_USERNAME`
If initializing the database it creates a datamanager username with the given username.

### `DATAMANAGER_PASSWORD`
If initializing the database it creates a datamanger password with the given password.

### `DATAMANAGER_FULL_NAME`
If initializing the database it creates a datamanager person with the given full name.

### `PORT`
Port where gunicorn will handle the requests. Defaults to 80. This might be needed if deploying in Heroku (where it sets it) otherwise changing the left part of the docker `--publish 8000:80` it should not be needed.
