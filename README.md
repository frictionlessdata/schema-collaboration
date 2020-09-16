[![C/I testing with coverage](https://github.com/frictionlessdata/schema-collaboration/workflows/C/I%20testing%20with%20coverage/badge.svg?branch=master)](https://github.com/frictionlessdata/schema-collaboration/actions)
[![Coverage Status](https://coveralls.io/repos/github/frictionlessdata/schema-collaboration/badge.svg?branch=master&service=github)](https://coveralls.io/github/frictionlessdata/schema-collaboration?branch=master)

# schema-collaboration
Carles Pina Estany's 2020 Tool Fund: data managers and researchers collaborate to write the Frictionless Data packages, tabular schemas, etc. 

More information: https://frictionlessdata.io/blog/2020/07/16/tool-fund-polar-institute/

See progress on https://github.com/frictionlessdata/schema-collaboration/wiki

An installation to play with: https://carles.eu.pythonanywhere.com

# Installation for development
This application is not ready to be used yet.

A Docker container and docker-compose.yml will exist to facilitate deployments.

At the moment certain familiarity with Django and databases is still needed.

```
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

python3 manage.py createsuperuser --username admin
```

Then visit http://127.0.0.1:8000/ to see the Welcome page.

## Setup the system: create the data manager user

Visit http://127.0.0.1:8000/admin and you can login using the `admin` user recently created. Then please create the datamanger user (this might be automated in the future):
 * Click on the left hand side panel on `Users`
 * Click on the top-right option "Add User"
 * Fill-in the Username and Password (e.g. `datamanager` or the name of the datamanager and a password). Click on `Save`
 * Click on the left hand side panel on `People`
 * Click on `Add Person`: in `Full name` enter the datamanger's full name. In `User` select the datamanger's User. Click on `Save`
 * Click on `Log out` (top-right hand side)
 * Optional: click on `Datapackage statuses` and add Data Package Status. Suggested status: `Draft`, `In Progress` and `Completed`. Feel free to create status that suits your institution
 * Visit http://127.0.0.1:8000/accounts/login/ and login as a datamanger
 * 

 At this point the system is usable for the datamanger. 
