from django.urls import path
from selia.views.create_views import collection_users


urlpatterns = [
    path(
        'collection_users/create/',
        collection_users.CreateCollectionUserManager.as_view(),
        name='create_collection_user'),
    path(
        'collection_users/create/1/',
        collection_users.SelectCollectionUserCollectionView.as_view(),
        name='create_collection_user_select_collection'),
    path(
        'collection_users/create/2/',
        collection_users.SelectCollectionUserUserView.as_view(),
        name='create_collection_user_select_user'),
    path(
        'collection_users/create/3/',
        collection_users.SelectCollectionUserRoleView.as_view(),
        name='create_collection_user_select_role'),
    path(
        'collection_users/create/4/',
        collection_users.CreateCollectionUserView.as_view(),
        name='create_collection_user_create_form'),
]
