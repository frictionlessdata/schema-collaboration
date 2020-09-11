from jinja2 import Template


# This is designed in a way that is independent of Django
# in order to be easy (but changes are required) to be used
# outside Django in the future

def datapackage_to_markdown(datapackage):
    template = Template(template_to_md)
    rendered = template.render(datapackage)
    print(rendered)


template_to_md = '''
NAME: {{ name }}
TITLE: {{ title }}

{% for contributor in contributors %}
    {{ contributor.title }}
{% endfor %}
'''
