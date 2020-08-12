from django.urls import path

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('schema/list/', views.SchemaList.as_view(), name='schema-list'),
    path('schema/<uuid:uuid>/', views.SchemaDetail.as_view(), name='schema-detail'),
    path('api/schema/', views.ApiSchemaView.as_view(), name='api-schema'),
    path('api/schema/<uuid:uuid>/', views.ApiSchemaView.as_view(), name='api-schema'),
    path('datapackage-ui/', views.DatapackageUi.as_view(), name='datapackage-ui'),
]
