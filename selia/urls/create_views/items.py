from django.urls import path
from selia.views.create_views import items


urlpatterns = [
    path(
        'items/create/',
        items.CreateItemManager.as_view(),
        name='create_item'),
    path(
        'items/create/1/',
        items.SelectItemCollectionView.as_view(),
        name='create_item_select_collection'),
    path(
        'items/create/2/',
        items.SelectItemSamplingEventView.as_view(),
        name='create_item_select_sampling_event'),
    path(
        'items/create/3/',
        items.SelectItemLicenceView.as_view(),
        name='create_item_select_licence'),
    path(
        'items/create/4/',
        items.SelectItemTypeView.as_view(),
        name='create_item_select_item_type')
]
