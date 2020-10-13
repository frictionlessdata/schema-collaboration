import os

from django import template
from django.conf import settings
from django.utils.html import escape
# Modified from: https://stackoverflow.com/a/34545839/9294284
from django.utils.safestring import mark_safe

register = template.Library()


def read_file(file_path):
    if file_path is None:
        return None

    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            string = f.read()
            return string
    else:
        return None


# Easy way to read a static file and input it in the template
@register.simple_tag
def includestatic(path, default):
    file_path = os.path.join(settings.STATIC_ROOT, path)

    file_content = read_file(file_path)

    if file_content is None:
        return default
    else:
        return escape(file_content)


@register.simple_tag
def includestaticextrajs():
    file_content = read_file(settings.EXTRA_JS_FILE)

    return mark_safe(file_content) if file_content else ''
