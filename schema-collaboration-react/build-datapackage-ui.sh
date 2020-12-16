#!/bin/bash -e

SCRIPT_BASE_DIRECTORY=$(dirname "${BASH_SOURCE[0]}")

SCHEMA_COLLABORATION_REACT_DIRECTORY="$SCRIPT_BASE_DIRECTORY"

cd "$SCHEMA_COLLABORATION_REACT_DIRECTORY"

if npm run build
then
	DESTINATION="$SCHEMA_COLLABORATION_REACT_DIRECTORY/../SchemaCollaboration/core/static/datapackage-ui/"
	
	git rm -rf "$DESTINATION"
	mkdir -p "$DESTINATION"

	rsync -rv --delete build/* ../SchemaCollaboration/core/static/datapackage-ui/
	echo "Do not edit files in this directory. This is the result of 'npm run build' in $SCHEMA_COLLABORATION_REACT_DIRECTORY. It is in the git repository to facilitate deployment and development of the Django part when it is not needed to change datapackage-ui code" > "$DESTINATION/README.md"
	git add "$SCHEMA_COLLABORATION_REACT_DIRECTORY/../SchemaCollaboration/core/static/datapackage-ui/"

else
	echo; echo
	echo "\"npm run build\" failed"
	echo "You might need to install the dependencies: npm install"
fi

