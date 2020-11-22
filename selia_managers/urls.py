from django.urls import path
from selia_managers import views
from selia_managers.views import list_views
from selia_managers.views import detail_views
from selia_managers.views import delete_views

from selia_managers.views.create_views import collection
from selia_managers.views.create_views import administrator

urlpatterns = [
    path('', views.CollectionManagementHome.as_view(), name='management'),
    path(
        'collections/',
        list_views.ManagedCollectionsListView.as_view(),
        name='collections'),
    path(
        'users/',
        list_views.ManagedUsersListView.as_view(),
        name='users'),
    path(
        'collections/<pk>/detail/',
        detail_views.DetailCollectionView.as_view(),
        name='collection_detail'),
    path(
        'collections/<pk>/users/',
        list_views.CollectionUsersListView.as_view(),
        name='collection_users'),
    path(
        'collections/<pk>/administrators/delete/',
        delete_views.delete_administrator,
        name='remove_administrator'),
    path(
        'collection/create/',
        collection.CreateCollectionManager.as_view(),
        name='create_collection'),
    path(
        'collection/create/1/',
        collection.SelectCollectionCollectionView.as_view(),
        name='create_collection_select_collection_type'),
    path(
        'collection/create/2/',
        collection.CreateCollectionView.as_view(),
        name='create_collection_create_form'),
    path(
        'administrator/create/',
        administrator.CreateAdministratorManager.as_view(),
        name='create_administrator'),
    path(
        'administrator/create/1/',
        administrator.SelectCollectionAdministratorView.as_view(),
        name='create_administrator_select_collection'),
    path(
        'administrator/create/2/',
        administrator.SelectUserAdministratorView.as_view(),
        name='create_administrator_select_user'),
    path(
        'administrator/create/3/',
        administrator.create_administrator_view,
        name='create_administrator_create_form'),
]
