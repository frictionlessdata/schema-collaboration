from django.views.generic import TemplateView
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class Homepage(TemplateView):
    template_name = 'core/homepage.html'


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        file_obj = request.data['file']
        f = open('/tmp/test.txt', 'wb')
        f.write(file_obj.file.read())
        f.close()
        return Response(status=204)
