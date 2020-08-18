from django.shortcuts import render
from django.views.generic import ListView

from core.models import Schema


class SchemaList(ListView):
    template_name = 'management/schema-list.html'
    model = Schema
    context_object_name = 'schemas'
