[![C/I testing with coverage](https://github.com/frictionlessdata/schema-collaboration/workflows/C/I%20testing%20with%20coverage/badge.svg?branch=master)](https://github.com/frictionlessdata/schema-collaboration/actions)
[![Coverage Status](https://coveralls.io/repos/github/frictionlessdata/schema-collaboration/badge.svg?branch=master&service=github)](https://coveralls.io/github/frictionlessdata/schema-collaboration?branch=master)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# schema-collaboration
Carles Pina Estany's 2020 Tool Fund: data managers and researchers collaborate to write the Frictionless Data packages and tabular schemas.

Current state: last features for the initial functional release are being finished. Feedback is welcomed (via [Github Issues](https://github.com/frictionlessdata/schema-collaboration/issues), [email](carles@pina.cat) or [Frictionless data Discord](https://discord.com/invite/Sewv6av).

More information about this tool fund in the [Frictionless Data Blog](https://frictionlessdata.io/blog/2020/07/16/tool-fund-polar-institute/)

See progress on the [log](https://github.com/frictionlessdata/schema-collaboration/wiki)

For demo purposes (not for real use) see the [installed schema-collaboration.](https://carles.eu.pythonanywhere.com). You also read the [data manager first steps](https://github.com/frictionlessdata/schema-collaboration/blob/master/documentation/User.md#schema-collaboration) documentation for an initial guidance.

Find below some basic documentation and also how to [install it using Docker](https://github.com/frictionlessdata/schema-collaboration/tree/master/docker#schema-collaboration-docker).

# Installation for development
## Server side Django
The application is implemented in Django. Steps to download, create the basic users and execute the server:

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

python3 manage.py create_datamanagement_and_admin_user \
	data_username \
	"DataManagerName DataManagerSurname" \
	data_manager_secret_pwd \
	admin_secret_pwd

python3 manage.py create_default_data_package_status # This will create default three status and can be changed at any time

python3 manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the homepage.

Visit [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) to see the management (for the data manager) section.

In order to use the PDF generation you need to install Pandoc with the suggested packages:
```sh
apt install pandoc
```

## Modification on datapackage-ui
This section is only important if a developer intends to modify the integration with datapackage-ui or update datapackage-ui. For example, adding buttons, change buttons/API, toaster, change the API communication between datapackage-ui and Django server, etc.

[datapackage-ui](https://github.com/frictionlessdata/datapackage-ui) is a dependency of schema-collaboration. It uses npm and React.

In the schema-repository repository there is an already built datapackage-ui in `SchemaCollaboration/core/static/datapackage-ui/`. If code changes do not affect datapackage-ui (files in `schema-collaboration-react`): no need to rebuild it.

If there are code changes in `schema-collaboration-react` then the `build-datapackage-ui.sh` needs to executed. This will build the static files of `datapackage-ui` and copy them into `SchemaCollaboration/core/static/datapackage-ui/`. Then you can commit then.

The reason of committing the static generated files is for convenience: it is easier to deploy and easier to modify schema-collaboration without having to install npm.
