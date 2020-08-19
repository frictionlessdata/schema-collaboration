from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('', views.SchemaList.as_view(), name='list-schemas'),
    path('person/list/', views.PersonList.as_view(), name='list-people'),

    path('person/add/', views.PersonCreate.as_view(), name='person-add'),
    path('person/<int:pk>/edit/', views.PersonUpdate.as_view(), name='person-update'),
    path('person/<int:pk>/delete/', views.PersonDelete.as_view(), name='person-delete'),

    path('person/<int:pk>/', views.PersonDetail.as_view(), name='person-detail'),

    path('datapackage/manage/<uuid:uuid>', views.DatapackageManage.as_view(), name='datapackage-manage'),
]
