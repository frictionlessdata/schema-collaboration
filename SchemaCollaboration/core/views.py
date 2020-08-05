from django.views.generic import TemplateView, ListView
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


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        file_obj = request.data['file']

        schema = Schema.objects.create(schema=file_obj.file.read())

        return Response(status=204)


class Ping(TemplateView):
    template_name = 'core/homepage.html'
