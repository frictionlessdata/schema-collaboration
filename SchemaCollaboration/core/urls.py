from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('datapackage/list/collaborator/<uuid:collaborator_uuid>/', views.DatapackageListView.as_view(),
         name='datapackage-list'),
    path('datapackage/<uuid:uuid>/', views.DatapackageDetailView.as_view(), name='datapackage-detail'),
    path('api/datapackage/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('api/datapackage/<uuid:uuid>/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('datapackage-ui/', views.DatapackageUiView.as_view(), name='datapackage-ui'),

    path('datapackage/<uuid:uuid>/add_comment/', views.DatapackageAddCommentView.as_view(),
         name='datapackage-add-comment'),

    path('accounts/', include('django.contrib.auth.urls')),
]
