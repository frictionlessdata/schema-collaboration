from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('', views.DatapackageListView.as_view(), name='list-schemas'),
    path('person/list/', views.PersonListView.as_view(), name='list-people'),

    path('person/add/', views.PersonCreateView.as_view(), name='person-add'),
    path('person/<int:pk>/edit/', views.PersonUpdateView.as_view(), name='person-update'),
    path('person/<int:pk>/delete/', views.PersonDeleteView.as_view(), name='person-delete'),

    path('person/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),

    path('datapackage/<int:pk>/', views.DatapackageDetailView.as_view(), name='datapackage-detail'),
    path('datapackage/<int:pk>/edit/', views.DatapackageUpdateView.as_view(), name='datapackage-update'),
    path('datapackage/<int:datapackage_id>/add_comment/', views.DatapackageAddCommentView.as_view(),
         name='datapackage-add-comment'),
]
