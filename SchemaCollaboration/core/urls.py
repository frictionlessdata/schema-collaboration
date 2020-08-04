from django.urls import path

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage')
]
