#!/bin/bash

SCRIPT_BASE_DIRECTORY=$(dirname "${BASH_SOURCE[0]}")

# rsync -arv "$SCRIPT_BASE_DIRECTORY/src" "$SCRIPT_BASE_DIRECTORY/../datapackage-ui"

cd "$SCRIPT_BASE_DIRECTORY/../datapackage-ui"

npm run build

mkdir -p ../SchemaCollaboration/core/static/datapackage-ui/dist
cp -r dist/* ../SchemaCollaboration/core/static/datapackage-ui/dist/
cp index.html ../SchemaCollaboration/core/static/datapackage-ui

