# schema-collaboration Docker

The Docker image created for this project can use an internal sqlite3 database (for testing) or for production it requires a MariaDB/MySQL database.

## Start a `schema-collaboration` server instance
Download the image:
```
$ docker pull cpina/schema-collaboration
```

### sqlite3 database
Execute it passing the environment variables to create the admin password and data manager user:
```
docker run \
    -e FORCE_SQLITE3_DATABASE=1 \
    -e ADMIN_PASSWORD=my_secret_pw \
    -e DATAMANAGER_USERNAME=data \
    -e DATAMANAGER_FULL_NAME="DataName DataSurname" \
    -e DATAMANAGER_PASSWORD=dm_secret_pwd
    cpina/schema-collaboration
```

**Warning:**: above command uses sqlite3 database. This is meant for testing and evaluating. For production use please use a MariaDB/MySQL server.

### MariaDB database
For this you need to have a MariaDB/MySQL server with a user to manage the database. This user should have privileges to create and drop tables in the database. In case of doubt check your database manual. As a quick reference execute on the SQL shelL with enough privileges:
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
    -e ADMIN_PASSWORD=my_secret_pw \
    -e DATAMANAGER_USERNAME=data \
    -e DATAMANAGER_FULL_NAME="DataName DataSurname" \
    -e DATAMANAGER_PASSWORD=dm_secret_pwd \
    -e DB_NAME=schema_collaboration \
    -e DB_USER=schema_collaboration \
    -e DB_PASSWORD=schema-collaboration-db-password \
    -e DB_HOST=localhost \
    -e DB_PORT=3306 \
    cpina/schema-collaboration
``` 

## Via `docker-compose`
An example file to be modified:
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

You can pass the 

## Production notes


## Environment variables
