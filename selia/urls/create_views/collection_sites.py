from django.urls import path
from selia.views.create_views import collection_sites


urlpatterns = [
    path(
        'collection_sites/create/',
        collection_sites.CreateCollectionSiteManager.as_view(),
        name='create_collection_site'),
    path(
        'collection_sites/create/1/',
        collection_sites.SelectCollectionSiteCollectionView.as_view(),
        name='create_collection_site_select_collection'),
    path(
        'collection_sites/create/2/',
        collection_sites.SelectCollectionSiteTypeView.as_view(),
        name='create_collection_site_select_type'),
    path(
        'collection_sites/create/3/',
        collection_sites.SelectCollectionSiteSiteView.as_view(),
        name='create_collection_site_select_site'),
    path(
        'collection_sites/create/4/',
        collection_sites.CollectionSiteCreateView.as_view(),
        name='create_collection_site_create_form'),
]
