from django.urls import path
from selia.views import detail_views


urlpatterns = [
    path(
        'collection_devices/detail/<pk>/',
        detail_views.DetailCollectionDeviceView.as_view(),
        name='collection_device_detail'),
    path(
        'collection_sites/detail/<pk>/',
        detail_views.DetailCollectionSiteView.as_view(),
        name='collection_site_detail'),
    path(
        'collection_users/detail/<pk>/',
        detail_views.DetailCollectionUserView.as_view(),
        name='collection_user_detail'),
    path(
        'collections/detail/<pk>/',
        detail_views.DetailCollectionView.as_view(),
        name='collection_detail'),
    path(
        'items/detail/<pk>/',
        detail_views.DetailItemView.as_view(),
        name='item_detail'),
    path(
        'licences/detail/<pk>/',
        detail_views.DetailLicenceView.as_view(),
        name='licence_detail'),
    path(
        'physical_devices/detail/<pk>/',
        detail_views.DetailPhysicalDeviceView.as_view(),
        name='physical_device_detail'),
    path(
        'sampling_event_devices/detail/<pk>/',
        detail_views.DetailSamplingEventDeviceView.as_view(),
        name='sampling_event_device_detail'),
    path(
        'sampling_events/detail/<pk>/',
        detail_views.DetailSamplingEventView.as_view(),
        name='sampling_event_detail'),
    path(
        'sites/detail/<pk>/',
        detail_views.DetailUserSiteView.as_view(),
        name='site_detail'),
    path(
        'user/',
        detail_views.DetailUserView.as_view(),
        name='user_home'),
]
