import os
import subprocess
from tempfile import NamedTemporaryFile

from jinja2 import Template


# This file designed in a way that is independent of Django
# in order to be easy (but changes are required) to be used
# outside Django in the future
# That's why is using jinja2 as a template language instead of
# Django's template language.

def datapackage_to_markdown(datapackage):
    """
    datapackage: datapackage schema as a dictionary
    returns: str with the Markdown documentation
    """
    template = Template(template_to_md)
    rendered = template.render(datapackage)

    return rendered.encode('utf-8')


def datapackage_to_pdf(datapackage):
    """
    datapackage: datapackage schema as a dictionary
    returns: binary content with the PDF or None if the conversion failed.
    """
    markdown = datapackage_to_markdown(datapackage)

    f = NamedTemporaryFile(suffix='.pdf', delete=False)
    f.close()

    command_line = ['pandoc', '--to=latex', f'--output={f.name}']

    try:
        pandoc_process = subprocess.run(command_line,
                                        input=markdown)
    except FileNotFoundError:
        os.unlink(f.name)
        raise OSError(f'FileNotFoundError trying to execute: {command_line}')
    except subprocess.CalledProcessError:
        os.unlink(f.name)
        raise RuntimeError(f'CalledProcessError trying to execute: {command_line}')

    if pandoc_process.returncode != 0:
        os.unlink(f.name)
        raise RuntimeError(f'Command {command_line} returned a PDF file of size 0')

    pdf_file = open(f.name, 'rb')

    pdf_content = pdf_file.read()
    os.unlink(f.name)

    return pdf_content


template_to_md = '''# {{ title }}

## Dataset description
{{ description }}
{% if contributors|length == 1 %}
## Contributor
{% else %}
## Contributors
{% endif %}{% for contributor in contributors %} * {{ contributor.title }} ({{ contributor.role }})
{% endfor %}{% if keywords|length == 1 %}
## Keyword
{% else %}## Keywords
{% endif %}{% for keyword in keywords %} * {{ keyword }}
{% endfor %}
## Version
{{ version }}

## Homepage
[{{ homepage }}]({{ homepage }})

## Data processing
TODO

## Quality checking
TODO
{% if licenses|length == 1 %}
## Dataset license
{% else %}
## Dataset license
{% endif %}{% for license in licenses %} * {{ license.title }} ([{{ license.name }}]({{ license.path }}))
{% endfor %}
## Dataset citation
TODO

## Resources
{% for resource in resources %}
### {{ resource.path }}
{% for field in resource.schema.fields %} * **{{ field.name }}** ({{ field.type }}): {{ field.description }}

{% endfor %} 
{% endfor %}
'''
