#!/bin/bash

cd datapackage-ui
npm run build
mkdir -p ../SchemaCollaboration/core/static/datapackage-ui/dist
cp -r dist/* ../SchemaCollaboration/core/static/datapackage-ui/dist/
cp index.html ../SchemaCollaboration/core/static/datapackage-ui

