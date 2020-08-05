from django.urls import path

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('api/upload/', views.FileUploadView.as_view(), name='schema-upload'),
    path('api/ping/', views.Ping.as_view(), name='ping')
]
