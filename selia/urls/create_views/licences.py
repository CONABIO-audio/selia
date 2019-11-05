from django.urls import path
from selia.views.create_views import licences


urlpatterns = [
    path(
        'licences/create/',
        licences.CreateLicenceManager.as_view(),
        name='create_licence'),
    path(
        'licences/create/1/',
        licences.SelectLicenceTypeView.as_view(),
        name='create_licence_select_type'),
    path(
        'licences/create/2/',
        licences.CreateLicenceView.as_view(),
        name='create_licence_create_form'),

]
