from django.urls import path, include
from django.contrib.auth import views as auth_views

from SchemaCollaboration import settings
from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('datapackage/list/collaborator/<uuid:collaborator_uuid>/', views.DatapackageListView.as_view(),
         name='datapackage-list'),
    path('datapackage/<uuid:uuid>/', views.DatapackageDetailView.as_view(), name='datapackage-detail'),
    path('api/datapackage/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('api/datapackage/<uuid:uuid>/', views.ApiSchemaView.as_view(), name='api-datapackage'),
    path('api/datapackage/<uuid:uuid>/markdown', views.ApiSchemaMarkdownView.as_view(), name='api-datapackage-markdown'),
    path('api/datapackage/<uuid:uuid>/pdf', views.ApiSchemaPdfView.as_view(), name='api-datapackage-pdf'),
    path('datapackage-ui/', views.DatapackageUiView.as_view(), name='datapackage-ui'),

    path('datapackage/<uuid:uuid>/add_comment/', views.DatapackageAddCommentView.as_view(),
         name='datapackage-add-comment'),

    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='registration/login.html',
                                      extra_context={'demo_username': settings.DEMO_USERNAME,
                                                     'demo_password': settings.DEMO_PASSWORD}),
         name='login'),

    path('accounts/', include('django.contrib.auth.urls')),
]
