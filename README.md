[![C/I testing with coverage](https://github.com/frictionlessdata/schema-collaboration/workflows/C/I%20testing%20with%20coverage/badge.svg?branch=master)](https://github.com/frictionlessdata/schema-collaboration/actions)
[![Coverage Status](https://coveralls.io/repos/github/frictionlessdata/schema-collaboration/badge.svg?branch=master&service=github)](https://coveralls.io/github/frictionlessdata/schema-collaboration?branch=master)

# schema-collaboration
Carles Pina Estany's 2020 Tool Fund: data managers and researchers collaborate to write the Frictionless Data packages, tabular schemas, etc. 

More information: https://frictionlessdata.io/blog/2020/07/16/tool-fund-polar-institute/

See progress on https://github.com/frictionlessdata/schema-collaboration/wiki

An installation to play with: https://carles.eu.pythonanywhere.com

schema-collaboration can be tested or deployed using Docker. See the Docker instructions: https://github.com/frictionlessdata/schema-collaboration/blob/master/docker/README.md

# Installation for development
This application is not ready to be used yet.

The application uses Django. Suggested steps:

```sh
git clone git@github.com:frictionlessdata/schema-collaboration.git
cd schema-collaboration
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd SchemaCollaboration

export SECRET_KEY=this_is_a_test
export ALLOWED_HOSTS=localhost,127.0.0.1
export FORCE_SQLITE3_DATABASE=1	# otherwise it would use Mysql/Mariadb and you need to setup DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

python3 manage.py migrate

python3 manage.py runserver

python3 manage.py create_datamanagement_user \
	data_username \
	"DataManagerName DataManagerSurname" \
	data_manager_secret_pwd \
	admin_secret_pwd

python3 manage.py create_status # This will create default three status and can be changed at any time
```

Visit http://127.0.0.1:8000/ to see the homepage.

Visit http://127.0.0.1:8000/accounts/login/ to see the management (for the data manager) section.

