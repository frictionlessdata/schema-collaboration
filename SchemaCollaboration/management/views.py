from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comments.forms import CommentForm
from comments.views import process_post_add_comment
from core.models import Datapackage, Person, DatapackageStatus
from core.views import datapackage_detail_context
from management.forms import PersonModelForm, DatapackageModelForm


class DatapackageListView(ListView):
    template_name = 'management/schema-list.html'
    model = Datapackage
    context_object_name = 'schemas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'datapackages'
        context['breadcrumb'] = [{'name': 'Datapackages'}]

        for schema in context['schemas']:
            schema.collaborator_view_link = self.request.build_absolute_uri(
                reverse('datapackage-detail', kwargs={'uuid': schema.uuid}))
            schema.edit_link = schema.generate_edit_link(self.request.path)

        return context


class PersonMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'collaborator'
        return context


def add_list_datapackage_url_to_person(person, request):
    person.list_datapackages_url = request.build_absolute_uri(
        reverse('datapackage-list', kwargs={'collaborator_uuid': person.uuid}
                ))


class CollaboratorListView(PersonMixin, ListView):
    template_name = 'management/person-list.html'
    model = Person
    context_object_name = 'collaborators'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'Collaborator'}]

        for collaborator in context['collaborators']:
            add_list_datapackage_url_to_person(collaborator, self.request)

        return context


class CollaboratorCreateView(PersonMixin, CreateView):
    model = Person
    form_class = PersonModelForm
    template_name = 'management/person-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'Collaborators', 'url': reverse('management:collaborator-list')},
                                 {'name': 'Create'}]
        return context


class CollaboratorUpdateView(PersonMixin, UpdateView):
    model = Person
    form_class = PersonModelForm
    template_name = 'management/person-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'Collaborators', 'url': reverse('management:collaborator-list')},
                                 {'name': 'Edit'}]
        return context


class CollaboratorDeleteView(DeleteView):
    model = Person
    success_url = reverse_lazy('management-list-collaborators')


class CollaboratorDetailView(PersonMixin, DetailView):
    model = Person
    template_name = 'management/person-detail.html'
    context_object_name = 'collaborator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'Collaborators', 'url': reverse('management:collaborator-list')},
                                 {'name': 'Detail'}]

        add_list_datapackage_url_to_person(context['collaborator'], self.request)

        return context


class DatapackageMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'datapackages'
        return context


class DatapackageCreate(DatapackageMixin, View):
    def get(self, request, *args, **kwargs):
        # Create an empty package - this is called from a link at the moment
        # it should change in the future?
        schema = Datapackage.objects.create(schema='')

        try:
            default_status_on_creation = DatapackageStatus.objects.get(
                behaviour=DatapackageStatus.StatusBehaviour.DEFAULT_ON_DATAPACKAGE_CREATION)
            schema.status = default_status_on_creation
            schema.save()
        except ObjectDoesNotExist:
            pass

        return redirect(schema.generate_edit_link(reverse('management:list-schemas')))


class DatapackageDetailView(DatapackageMixin, DetailView):
    model = Datapackage
    template_name = 'management/datapackage-detail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumb'] = [{'name': 'Datapackages', 'url': reverse('management:list-schemas')},
                                 {'name': 'Detail'}]

        person = Person.objects.get(user=self.request.user)

        context['comment_form'] = CommentForm(person=person,
                                              datapackage_id=self.object.id,
                                              allow_private=True,
                                              form_action_url=reverse('management:datapackage-add-comment',
                                                                      kwargs={'uuid': self.object.uuid}))

        context['comments'] = self.object.comments_for_management()
        context['show_private_field'] = True
        return context


class DatapackageUpdateView(DatapackageMixin, UpdateView):
    model = Datapackage
    form_class = DatapackageModelForm
    template_name = 'management/datapackage-form.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('management:datapackage-detail', kwargs={'uuid': self.object.uuid})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'Datapackages', 'url': reverse('management:collaborator-list')},
                                 {'name': 'Edit'}]
        return context


class DatapackageAddCommentView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        datapackage = Datapackage.objects.get(uuid=kwargs['uuid'])
        context = datapackage_detail_context(datapackage)

        return process_post_add_comment(request,
                                        context,
                                        datapackage=datapackage,
                                        force_anonymous_user=False,
                                        success_view_name='management:datapackage-detail',
                                        failure_template_name='core/datapackage-detail.html')
