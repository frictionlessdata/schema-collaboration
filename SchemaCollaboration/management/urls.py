from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('', views.DatapackageList.as_view(), name='list-schemas'),
    path('person/list/', views.PersonList.as_view(), name='list-people'),

    path('person/add/', views.PersonCreate.as_view(), name='person-add'),
    path('person/<int:pk>/edit/', views.PersonUpdate.as_view(), name='person-update'),
    path('person/<int:pk>/delete/', views.PersonDelete.as_view(), name='person-delete'),

    path('person/<int:pk>/', views.PersonDetail.as_view(), name='person-detail'),

    path('datapackage/<int:pk>/', views.DatapackageDetail.as_view(), name='datapackage-detail'),
    path('datapackage/<int:pk>/edit/', views.DatapackageUpdate.as_view(), name='datapackage-update'),
]
