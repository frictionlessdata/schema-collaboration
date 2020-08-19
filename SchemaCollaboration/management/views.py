from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.models import Schema, Person
from management.forms import PersonModelForm


class SchemaList(ListView):
    template_name = 'management/schema-list.html'
    model = Schema
    context_object_name = 'schemas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'datapackages'
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


class PersonCreate(CreateView):
    model = Person
    form_class = PersonModelForm
    template_name = 'management/person-create.html'


class PersonUpdate(UpdateView):
    model = Person
    form_class = PersonModelForm
    template_name = 'management/person-create.html'


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('management-list-people')


class PersonDetail(PersonMixin, DetailView):
    model = Person
    template_name = 'management/person-detail.html'
