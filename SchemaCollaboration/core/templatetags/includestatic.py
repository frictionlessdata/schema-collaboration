import os

from django import template
from django.conf import settings
from django.utils.html import escape
# Modified from: https://stackoverflow.com/a/34545839/9294284
from django.utils.safestring import mark_safe

register = template.Library()


def read_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            string = f.read()
            return string
    else:
        return None


# Easy way to read a static file and input it in the template
@register.simple_tag
def includestatic(path):
    file_path = os.path.join(settings.STATIC_ROOT, path)

    return escape(read_file(file_path)) or None


@register.simple_tag
def includestaticextrajs():
    return mark_safe(read_file(settings.EXTRA_JS_FILE)) or ''
