from jinja2 import Template


# This is designed in a way that is independent of Django
# in order to be easy (but changes are required) to be used
# outside Django in the future

def datapackage_to_markdown(datapackage):
    template = Template(template_to_md)
    rendered = template.render(datapackage)

    return rendered


template_to_md = '''
# NAME
{{ name }}

# TITLE
{{ title }}

Contributors: {% for contributor in contributors %}{{ contributor.title }} ({{ contributor.role }}){% endfor %}

# Resources
{% for resource in resources %}
## {{ resource.name }}
### Fields
{% for field in resource.schema.fields %}
#### {{ field.name }}

Type: {{ field.type }}

Format: {{ field.format }}

Description: {{ field.description }}

{% endfor %} 
{% endfor %}
'''
