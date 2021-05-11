from django.urls import path
from selia.views import list_views


urlpatterns = [
    path(
        "collections/detail/<name>/devices/",
        list_views.ListCollectionDevicesView.as_view(),
        name="collection_devices",
    ),
    path(
        "collections/detail/<name>/items/",
        list_views.ListCollectionItemsView.as_view(),
        name="collection_items",
    ),
    path(
        "collections/detail/<name>/sites/",
        list_views.ListCollectionSitesView.as_view(),
        name="collection_sites",
    ),
    path(
        "collections/detail/<name>/users/",
        list_views.ListCollectionUserView.as_view(),
        name="collection_users",
    ),
    path(
        "collections/detail/<name>/licences/",
        list_views.ListCollectionLicencesView.as_view(),
        name="collection_licences",
    ),
    path(
        "collections/open_collections/",
        list_views.ListOpenCollectionsView.as_view(),
        name="open_collections",
    ),
    path(
        "sampling_events/detail/<pk>/deployments/",
        list_views.ListDeploymentsView.as_view(),
        name="sampling_event_deployments",
    ),
    path(
        "collections_devices/detail/<pk>/deployments/",
        list_views.ListDeviceDeploymentsView.as_view(),
        name="device_deployments",
    ),
    path(
        "sampling_events/detail/<pk>/devices/",
        list_views.ListDeploymentsView.as_view(),
        name="sampling_event_devices",
    ),
    #path(
    #    "sampling_events/detail/<pk>/items/",
    #    list_views.ListSamplingEventItemsView.as_view(),
    #    name="sampling_event_items",
    #),
    path(
        "collections/detail/<name>/sampling_events/",
        list_views.ListCollectionSamplingEventView.as_view(),
        name="collection_sampling_events",
    ),
    path(
        "collections/user_collections/",
        list_views.ListUserCollectionsView.as_view(),
        name="user_collections",
    ),
]
