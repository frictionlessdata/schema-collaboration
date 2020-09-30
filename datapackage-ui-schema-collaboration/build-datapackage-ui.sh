#!/bin/bash -e

SCRIPT_BASE_DIRECTORY=$(dirname "${BASH_SOURCE[0]}")

rsync -arv "$SCRIPT_BASE_DIRECTORY/patch/" "$SCRIPT_BASE_DIRECTORY/../datapackage-ui"

mkdir -p "$SCRIPT_BASE_DIRECTORY/../SchemaCollaboration/core/static/datapackage-ui/dist"

cp "$SCRIPT_BASE_DIRECTORY/patch/index.html" "../SchemaCollaboration/core/static/datapackage-ui"

cd "$SCRIPT_BASE_DIRECTORY/../datapackage-ui"
npm run build
cp -r dist/* ../SchemaCollaboration/core/static/datapackage-ui/dist/

