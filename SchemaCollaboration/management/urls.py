from django.urls import path

from . import views

urlpatterns = [
    path('management/', views.SchemaList.as_view(), name='management-list-schemas'),
    path('management/person/', views.PersonList.as_view(), name='management-list-people'),

    path('management/person/add/', views.PersonCreate.as_view(), name='management-person-add'),
    path('management/person/<int:pk>/', views.PersonUpdate.as_view(), name='management-person-update'),
    path('management/<int:pk>/delete/', views.PersonDelete.as_view(), name='management-person-delete'),

    path('management/person/<int:pk>/detail/', views.PersonDetail.as_view(), name='management-person-detail'),
]