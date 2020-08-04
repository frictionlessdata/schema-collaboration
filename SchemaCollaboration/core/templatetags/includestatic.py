import os

from django import template
from django.conf import settings
from django.utils.html import escape

# Modified from: https://stackoverflow.com/a/34545839/9294284

register = template.Library()


# Easy way to read a static file and input it in the template
@register.simple_tag
def includestatic(path):
    file_path = os.path.join(settings.STATIC_ROOT, path)

    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            string = f.read()
            return escape(string)
    else:
        return None
