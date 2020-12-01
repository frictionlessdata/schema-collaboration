from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.templatetags.includestatic import read_file

register = template.Library()


@register.simple_tag
def include_homepage():
    content = ''
    if settings.HOMEPAGE_FILE is None:
        content = f'''
        <h1>Welcome to schema-collaboration</h1>
        <p>
            This is the default homepage. Set the environment variable <span style="font-family: monospace;">DEFAULT_HOMEPAGE</span> point at an HTML file to change it.
        </p>
        
        <h2>What can you do?</h2>
        <ul>
            <li>The data manager can create people, datapackages and assign people to datapackages using the <a
                    href="{reverse('login')}">management area</a> (login required available on the next page).
            </li>
        </ul>
    '''
    else:
        file_content = read_file(settings.HOMEPAGE_FILE)
        if file_content is None:
            content = f'''Cannot load {settings.HOMEPAGE_FILE}. Please make sure that it exist and is readable by schema-collaboration.'''
        else:
            content = file_content

    return mark_safe(content)
