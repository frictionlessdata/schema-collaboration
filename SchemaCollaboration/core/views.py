from django.http import HttpResponse
from django.templatetags.static import static
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, RedirectView

from .models import Schema


class Homepage(TemplateView):
    template_name = 'core/homepage.html'


class SchemaList(ListView):
    template_name = 'core/schema-list.html'
    model = Schema
    context_object_name = 'schemas'


class SchemaDetail(DetailView):
    template_name = 'core/schema-detail.html'
    model = Schema
    context_object_name = 'schema'

    def get_object(self, queryset=None):
        return Schema.objects.get(uuid=self.kwargs['uuid'])


class FileUploadView(View):
    def post(self, request, *args, **kwargs):
        body = request.body
        Schema.objects.create(schema=body)
        return HttpResponse(status=204)


class FileGetView(View):
    model = Schema

    def get_object(self, queryset=None):
        return Schema.objects.get(uuid=self.kwargs['uuid'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.object.schema
        response = HttpResponse(status=200, content=data)
        response['Content-Type'] = 'application/json'
        return response

    def put(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        body = request.body

        schema = Schema.objects.get(uuid=uuid)
        schema.schema = body
        schema.save()

        response = HttpResponse(status=201)
        return response


class DatapackageUi(RedirectView):
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
