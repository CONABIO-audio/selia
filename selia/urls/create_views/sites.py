from django.urls import path
from selia.views.create_views import sites


urlpatterns = [
    path(
        'sites/create/',
        sites.CreateSiteManager.as_view(),
        name='create_site'),
    path(
        'sites/create/1/',
        sites.CreateSiteView.as_view(),
        name='create_site_create_form'),
]
