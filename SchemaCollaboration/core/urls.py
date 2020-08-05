from django.urls import path

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('api/upload/', views.FileUploadView.as_view(), name='schema-upload')
]
