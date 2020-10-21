from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('', views.DatapackageListView.as_view(), name='list-schemas'),
    path('collaborator/list/', views.CollaboratorListView.as_view(), name='collaborator-list'),

    path('collaborator/add/', views.CollaboratorCreateView.as_view(), name='collaborator-add'),
    path('collaborator/<int:pk>/edit/', views.CollaboratorUpdateView.as_view(), name='collaborator-update'),
    path('collaborator/<int:pk>/delete/', views.CollaboratorDeleteView.as_view(), name='collaborator-delete'),

    path('collaborator/<int:pk>/', views.CollaboratorDetailView.as_view(), name='collaborator-detail'),

    path('datapackage/create/', views.DatapackageCreate.as_view(), name='datapackage-create'),
    path('datapackage/<uuid:uuid>/', views.DatapackageDetailView.as_view(), name='datapackage-detail'),
    path('datapackage/<uuid:uuid>/edit/', views.DatapackageUpdateView.as_view(), name='datapackage-update'),
    path('datapackage/<uuid:uuid>/add_comment/', views.DatapackageAddCommentView.as_view(),
         name='datapackage-add-comment'),
]
