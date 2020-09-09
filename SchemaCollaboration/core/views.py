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
from comments.views import AbstractAddCommentView
from .models import Datapackage, Person


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


class DatapackageDetailView(DetailView):
    template_name = 'core/datapackage-detail.html'
    model = Datapackage
    context_object_name = 'datapackage'

    def get_object(self, queryset=None):
        return Datapackage.objects.get(uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        datapackage_id = context['datapackage'].id

        context['comment_form'] = CommentForm(person=None,
                                              datapackage_id=self.object.id,
                                              form_action_url=reverse('datapackage-add-comment',
                                                                      kwargs={'uuid': str(self.object.uuid)}))

        return context


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


class DatapackageAddCommentView(AbstractAddCommentView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, user=None,
                         success_view_name='datapackage-detail',
                         failure_url=None, **kwargs)
