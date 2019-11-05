from django.urls import path
from selia.views.create_views import collection_devices


urlpatterns = [
    path(
        'collection_devices/create/',
        collection_devices.CreateCollectionDeviceManager.as_view(),
        name='create_collection_device'),
    path(
        'collection_devices/create/1/',
        collection_devices.SelectCollectionDeviceCollectionView.as_view(),
        name='create_collection_device_select_collection'),
    path(
        'collection_devices/create/2/',
        collection_devices.SelectCollectionDevicePhysicalDeviceView.as_view(),
        name='create_collection_device_select_device'),
    path(
        'collection_devices/create/3/',
        collection_devices.CreateCollectionDeviceView.as_view(),
        name='create_collection_device_create_form'),
]
