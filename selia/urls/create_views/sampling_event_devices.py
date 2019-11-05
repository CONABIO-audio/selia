from django.urls import path
from selia.views.create_views import sampling_event_devices


urlpatterns = [
    path(
        'sampling_event_devices/create/',
        sampling_event_devices.CreateSamplingEventDeviceManager.as_view(),
        name='create_sampling_event_device'),
    path(
        'sampling_event_devices/create/1/',
        sampling_event_devices.SelectSamplingEventDeviceCollectionView.as_view(),
        name='create_sampling_event_device_select_collection'),
    path(
        'sampling_event_devices/create/2/',
        sampling_event_devices.SelectSamplingEventDeviceSamplingEventView.as_view(),
        name='create_sampling_event_device_select_sampling_event'),
    path(
        'sampling_event_devices/create/3/',
        sampling_event_devices.SelectSamplingEventDeviceCollectionDeviceView.as_view(),
        name='create_sampling_event_device_select_collection_device'),
    path(
        'sampling_event_devices/create/4/',
        sampling_event_devices.CreateSamplingEventDeviceView.as_view(),
        name='create_sampling_event_device_create_form'),
]
