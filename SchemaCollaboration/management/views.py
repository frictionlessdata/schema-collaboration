from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comments.forms import CommentForm
from core.models import Datapackage, Person
from management.forms import PersonModelForm, DatapackageModelForm


class DatapackageList(ListView):
    template_name = 'management/schema-list.html'
    model = Datapackage
    context_object_name = 'schemas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'datapackages'
        context['breadcrumb'] = [{'name': 'Datapackages'}]

        for schema in context['schemas']:
            schema.edit_link = self.request.build_absolute_uri(f'{reverse("datapackage-ui")}?load={schema.uuid}')

        return context


class PersonMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'people'
        return context


class PersonList(PersonMixin, ListView):
    template_name = 'management/person-list.html'
    model = Person
    context_object_name = 'people'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'People'}]

        for person in context['people']:
            person.list_datapackages_url = self.request.build_absolute_uri(
                reverse('datapackage-list', kwargs={'collaborator_uuid': person.uuid}
                        ))

        return context


class PersonCreate(PersonMixin, CreateView):
    model = Person
    form_class = PersonModelForm
    template_name = 'management/person-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'People', 'url': reverse('management:list-people')},
                                 {'name': 'Create'}]
        return context


class PersonUpdate(PersonMixin, UpdateView):
    model = Person
    form_class = PersonModelForm
    template_name = 'management/person-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'People', 'url': reverse('management:list-people')},
                                 {'name': 'Edit'}]
        return context


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('management-list-people')


class PersonDetail(PersonMixin, DetailView):
    model = Person
    template_name = 'management/person-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'People', 'url': reverse('management:list-people')},
                                 {'name': 'Detail'}]
        return context


class DatapackageMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'datapackages'
        return context


class DatapackageDetail(DatapackageMixin, DetailView):
    model = Datapackage
    template_name = 'management/datapackage-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumb'] = [{'name': 'Datapackage', 'url': reverse('management:list-schemas')},
                                 {'name': 'Detail'}]

        person = Person.objects.get(user=self.request.user)

        context['comment_form'] = CommentForm(person=person, datapackage_id=self.object.id)

        return context


class DatapackageUpdate(DatapackageMixin, UpdateView):
    model = Datapackage
    form_class = DatapackageModelForm
    template_name = 'management/datapackage-form.html'

    def get_success_url(self):
        return reverse('management:datapackage-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'name': 'Datapackage', 'url': reverse('management:list-people')},
                                 {'name': 'Edit'}]
        return context
