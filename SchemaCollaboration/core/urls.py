from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('datapackage/list/', views.DatapackageList.as_view(), name='schema-list'),
    path('datapackage/<uuid:uuid>/', views.DatapackageDetail.as_view(), name='schema-detail'),
    path('api/datapackage/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('api/datapackage/<uuid:uuid>/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('datapackage-ui/', views.DatapackageUi.as_view(), name='datapackage-ui'),

    path('accounts/', include('django.contrib.auth.urls')),
]
