from django.urls import path

from . import views

urlpatterns = [
    path('management/', views.SchemaList.as_view(), name='management-list-schemas'),
]
