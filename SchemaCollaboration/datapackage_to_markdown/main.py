import os
import subprocess
from tempfile import NamedTemporaryFile

from jinja2 import Template


# This is designed in a way that is independent of Django
# in order to be easy (but changes are required) to be used
# outside Django in the future

def datapackage_to_markdown(datapackage):
    template = Template(template_to_md)
    rendered = template.render(datapackage)

    return rendered


def datapackage_to_pdf(datapackage):
    markdown = datapackage_to_markdown(datapackage)

    f = NamedTemporaryFile(suffix='.pdf', delete=False)
    f.close()

    subprocess.run(['pandoc', '-t', 'latex', '-o', f.name],
                   input=markdown.encode('utf-8'))

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
