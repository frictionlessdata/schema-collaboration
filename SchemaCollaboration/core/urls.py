from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('datapackage/list/collaborator/<uuid:collaborator_uuid>/', views.DatapackageList.as_view(), name='datapackage-list'),
    path('datapackage/<uuid:uuid>/', views.DatapackageDetail.as_view(), name='datapackage-detail'),
    path('api/datapackage/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('api/datapackage/<uuid:uuid>/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('datapackage-ui/', views.DatapackageUi.as_view(), name='datapackage-ui'),

    path('datapackage/<uuid:uuid>/add_comment/', views.DatapackageAddComment.as_view(), name='datapackage-add-comment'),

    path('accounts/', include('django.contrib.auth.urls')),
]
