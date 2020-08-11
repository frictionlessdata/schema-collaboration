from django.http import HttpResponse
from django.templatetags.static import static
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

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


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        file_obj = request.data['file']

        schema = Schema.objects.create(schema=file_obj.file.read())

        return Response(status=204)


class FileGetView(DetailView):
    model = Schema

    def get_object(self, queryset=None):
        return Schema.objects.get(uuid=self.kwargs['uuid'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.object.schema
        response = HttpResponse(status=200, content=data)
        response['Content-Type'] = 'application/json'
        return response


class DatapackageUi(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        # TODO: Generalise this? to allow any number of parameters and not only uuid
        uuid = self.request.GET.get('load')
        return static('datapackage-ui/index.html') + f'?load={uuid}'
