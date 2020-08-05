from django.urls import path

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('schema/list/', views.SchemaList.as_view(), name='schema-list'),
    path('schema/<uuid:uuid>/', views.SchemaDetail.as_view(), name='schema-detail'),
    path('api/upload/', views.FileUploadView.as_view(), name='schema-upload'),
    path('api/ping/', views.Ping.as_view(), name='ping')
]
