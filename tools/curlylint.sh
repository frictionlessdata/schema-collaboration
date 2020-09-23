#!/bin/bash

# --rule 'indent: "tab"' Disabled, doesn't apply

curlylint --include '\.html' \
	--rule 'html_has_lang: "en"' \
	--rule 'aria_role: true' \
	--rule 'django_forms_rendering: true' \
	--rule 'image_alt: true' \
	--rule 'meta_viewport: true' \
	--rule 'no_autofocus: true' \
	--rule 'tabindex_no_positive: true' \
	SchemaCollaboration/core/templates \
	SchemaCollaboration/management/templates \
	SchemaCollaboration/comments/templates \
