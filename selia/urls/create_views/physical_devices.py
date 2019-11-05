from django.urls import path
from selia.views.create_views import physical_devices


urlpatterns = [
    path(
        'physical_devices/create/',
        physical_devices.CreatePhysicalDeviceManager.as_view(),
        name='create_physical_device'),
    path(
        'physical_devices/create/1/',
        physical_devices.SelectPhysicalDeviceDeviceView.as_view(),
        name='create_physical_device_select_device'),
    path(
        'physical_devices/create/2/',
        physical_devices.CreatePhysicalDeviceView.as_view(),
        name='create_physical_device_create_form'),
]
