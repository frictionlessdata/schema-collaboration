from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, RedirectView

from .models import Datapackage


class Homepage(TemplateView):
    template_name = 'core/homepage.html'


class DatapackageList(ListView):
    template_name = 'core/datapackage-list.html'
    model = Datapackage
    context_object_name = 'schemas'


class DatapackageDetail(DetailView):
    template_name = 'core/datapackage-detail.html'
    model = Datapackage
    context_object_name = 'schema'

    def get_object(self, queryset=None):
        return Datapackage.objects.get(uuid=self.kwargs['uuid'])


@method_decorator(csrf_exempt, name='dispatch')
class ApiSchemaView(View):
    def get(self, request, *args, **kwargs):
        schema = Datapackage.objects.get(uuid=self.kwargs['uuid'])
        response = HttpResponse(status=200, content=schema.schema)
        response['Content-Type'] = 'application/json'
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

        data = {'uuid': str(schema.uuid)}
        return JsonResponse(data, status=200)


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
