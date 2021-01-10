import json
from json import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, RedirectView

from comments.forms import CommentForm
from comments.views import process_post_add_comment
from datapackage_to_documentation.main import datapackage_to_markdown, datapackage_to_pdf
from .models import Datapackage, Person


def remove_prefix(text):
    # In Python 3.9+ has removeprefix straight away
    # https://stackoverflow.com/a/16891438/9294284

    prefix = 'text/json;charset=utf-8,'

    if text.startswith(prefix):  # only modify the text if it starts with the prefix
        text = text.replace(prefix, "", 1)  # remove one instance of prefix
    return text


def get_name_from_datapackage(body):
    """
    Returns a name of the datapackage. It's the field name if it has it,
    else it is a concatenation of the resources.
    """
    try:
        body_json = json.loads(body)
    except JSONDecodeError:
        return None

    name = body_json.get('name', None)

    if name is None:
        resources = body_json.get('resources', None)

        if isinstance(resources, list):
            resource_names = []
            for resource in resources:
                resource_names.append(resource['name'])

            name = ', '.join(resource_names)

    return name


class HomepageView(TemplateView):
    template_name = 'core/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            sheldon_cooper = Person.objects.get(full_name='Sheldon Cooper')
            uuid = sheldon_cooper.uuid
        except ObjectDoesNotExist:
            uuid = None

        context['example_collaborator_uuid'] = uuid
        return context


class DatapackageListView(ListView):
    template_name = 'core/datapackage-list.html'
    model = Datapackage
    context_object_name = 'schemas'

    def _get_collaborator(self):
        return get_object_or_404(Person, uuid=self.kwargs['collaborator_uuid'])

    def get_queryset(self):
        collaborator = get_object_or_404(Person, uuid=self.kwargs['collaborator_uuid'])
        return Datapackage.objects.filter(collaborators=self._get_collaborator())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collaborator'] = self._get_collaborator()

        for schema in context['schemas']:
            schema.collaborators_excluding_self_str = schema.collaborators_excluding_str(context['collaborator'])

        return context


def datapackage_detail_context(datapackage, logged_user):
    context = {}
    context['comment_form'] = CommentForm(logged_user=logged_user,
                                          datapackage_id=datapackage.id,
                                          form_action_url=reverse('datapackage-add-comment',
                                                                  kwargs={'uuid': str(datapackage.uuid)}))

    context['comments'] = datapackage.comments_for_collaborators()

    context['show_private_field'] = False

    return context


class DatapackageDetailView(DetailView):
    template_name = 'core/datapackage-detail.html'
    model = Datapackage
    context_object_name = 'datapackage'

    def get_object(self, queryset=None):
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])

        return schema

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        datapackage = kwargs['object']
        datapackage.edit_link = datapackage.generate_edit_link(self.request.path)

        context.update(datapackage_detail_context(datapackage, self.request.user))

        return context


@method_decorator(csrf_exempt, name='dispatch')
class ApiSchemaView(View):
    def get(self, request, *args, **kwargs):
        download = self.request.GET.get('dl', False)
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])
        response = HttpResponse(status=200, content=schema.schema)

        response['Content-Type'] = 'application/json'

        if download:
            name = schema.file_name(extension='json')
            response['Content-Disposition'] = f'attachment; filename="{name}"'
        return response

    def put(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        body = request.body.decode('utf-8')

        body = remove_prefix(body)

        schema = Datapackage.objects.get(uuid=uuid)

        name = get_name_from_datapackage(body)

        schema.name = name if name is not None else ''
        schema.schema = body
        schema.save()

        data = {'uuid': str(schema.uuid)}
        return JsonResponse(data, status=200)


class ApiSchemaMarkdownView(View):
    def get(self, request, *args, **kwargs):
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])

        markdown = datapackage_to_markdown(json.loads(schema.schema))

        response = HttpResponse(status=200, content=markdown)
        response['Content-Type'] = 'text/plain; charset=UTF-8'

        name = schema.file_name(extension='md')
        response['Content-Disposition'] = f'attachment; filename="{name}"'

        return response


class ApiSchemaPdfView(View):
    def get(self, request, *args, **kwargs):
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])

        try:
            pdf = datapackage_to_pdf(json.loads(schema.schema))
        except (RuntimeError, OSError) as e:
            response = HttpResponse(status=500,
                                    content=f'Cannot generate PDF: {e.args[0]}. Content the system administrator')
            return response

        response = HttpResponse(status=200, content=pdf)
        response['Content-Type'] = 'application/pdf'
        name = schema.file_name(extension='pdf')
        response['Content-Disposition'] = f'attachment; filename="{name}"'

        return response


class DatapackageUiView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        get_query_params = ''
        for url_param, url_value in self.request.GET.items():
            if get_query_params:
                get_query_params += '&'

            get_query_params += f'{url_param}={url_value}'

        return static('datapackage-ui/index.html') + '?' + get_query_params


class DatapackageAddCommentView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        datapackage = Datapackage.objects.get(uuid=kwargs['uuid'])
        context = datapackage_detail_context(datapackage, self.request.user)

        return process_post_add_comment(request,
                                        context,
                                        datapackage=datapackage,
                                        force_anonymous_user=True,
                                        success_view_name='datapackage-detail',
                                        failure_template_name='core/datapackage-detail.html')
