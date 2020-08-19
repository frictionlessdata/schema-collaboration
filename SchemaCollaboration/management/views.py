from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.models import Datapackage, Person
from management.forms import PersonModelForm, DatapackageModelForm


class SchemaList(ListView):
    template_name = 'management/schema-list.html'
    model = Datapackage
    context_object_name = 'schemas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'datapackages'
        context['breadcrumb'] = [{'name': 'Datapackages'}]
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


class DatapackageManage(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SchemaMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'people'
        return context


class DatapackageDetail(SchemaMixin, DetailView):
    model = Datapackage
    template_name = 'management/datapackage-detail.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumb'] = [{'name': 'Datapackage', 'url': reverse('management:list-schemas')},
                                 {'name': 'Detail'}]

        return context


class DatapackageUpdate(SchemaMixin, UpdateView):
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
