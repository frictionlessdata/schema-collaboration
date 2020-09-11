import json
import subprocess
from tempfile import NamedTemporaryFile

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
from .models import Datapackage, Person

from datapackage_to_markdown.main import datapackage_to_markdown

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


def datapackage_detail_context(datapackage):
    context = {}
    context['comment_form'] = CommentForm(person=None,
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
        return Datapackage.objects.get(uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        datapackage = kwargs['object']
        context.update(datapackage_detail_context(datapackage))

        return context


@method_decorator(csrf_exempt, name='dispatch')
class ApiSchemaView(View):
    def get(self, request, *args, **kwargs):
        download = self.request.GET.get('dl', False)
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])
        response = HttpResponse(status=200, content=schema.schema)

        response['Content-Type'] = 'application/json'

        if download:
            date = f'{schema.modified_on:%Y%m%d-%H%M}'
            if schema.name:
                name = f'{schema.name.replace(" ", "_")}-{date}.json'
            else:
                name = f'unnamed-{date}.json'

            response['Content-Disposition'] = f'attachment; filename="{name}"'
        return response

    def put(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        body = request.body.decode('utf-8')

        schema = Datapackage.objects.get(uuid=uuid)
        schema.schema = body
        schema.save()

        data = {'uuid': str(schema.uuid)}
        return JsonResponse(data, status=200)

    def post(self, request, *args, **kwargs):
        body = request.body.decode('utf-8')
        schema = Datapackage.objects.create(schema=body)

        response = HttpResponse(status=200, content='hello test carles')
        return response


@method_decorator(csrf_exempt, name='dispatch')
class ApiSchemaMarkdownView(View):
    def get(self, request, *args, **kwargs):
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])

        markdown = datapackage_to_markdown(json.loads(schema.schema))

        response = HttpResponse(status=200, content=markdown)
        response['Content-Type'] = 'text/plain; charset=UTF-8'

        return response


@method_decorator(csrf_exempt, name='dispatch')
class ApiSchemaPdfView(View):
    def get(self, request, *args, **kwargs):
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])

        markdown = datapackage_to_markdown(json.loads(schema.schema))

        # This is a draft and needs to be done differently (at least streaming the file? catching exceptions and
        # deleting the file? control errors if no pandoc/LaTeX, etc.)

        f = NamedTemporaryFile(suffix='.pdf', delete=False)
        f.close()

        process = subprocess.run(['pandoc', '-t', 'latex', '-o', f.name],
                                 input=markdown.encode('utf-8'))

        output = open(f.name, 'rb').read()

        response = HttpResponse(status=200, content=output)
        response['Content-Type'] = 'application/pdf'

        return response



class DatapackageUiView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        # TODO: Generalise this? to allow any number of parameters and not only uuid
        uuid = self.request.GET.get('load')

        if uuid:
            get_query_params = f'?load={uuid}'
        else:
            get_query_params = ''

        return static('datapackage-ui/index.html') + get_query_params


class DatapackageAddCommentView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        datapackage = Datapackage.objects.get(uuid=kwargs['uuid'])
        context = datapackage_detail_context(datapackage)

        return process_post_add_comment(request,
                                        context,
                                        datapackage=datapackage,
                                        force_anonymous_user=True,
                                        success_view_name='datapackage-detail',
                                        failure_template_name='core/datapackage-detail.html')
