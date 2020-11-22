from django.urls import path

from selia_user_home.views import create_views
from selia_user_home.views import detail_views
from selia_user_home.views import list_views

urlpatterns = [
    path("", detail_views.DetailUserView.as_view(), name="home"),
    path("items/", list_views.ListItemsView.as_view(), name="items"),
    path(
        "sampling_events/",
        list_views.ListSamplingEventsView.as_view(),
        name="sampling_events",
    ),
    path("sites/", list_views.ListSitesView.as_view(), name="sites"),
    path(
        "sites/detail/<pk>/",
        detail_views.DetailSiteView.as_view(),
        name="site_detail",
    ),
    path("sites/create/", create_views.CreateSiteManager.as_view(), name="create_site"),
    path(
        "sites/create/1/",
        create_views.SelectGeometryTypeView.as_view(),
        name="create_site_select_geometry_type",
    ),
    path(
        "sites/create/2/",
        create_views.CreateSiteView.as_view(),
        name="create_site_create_form",
    ),
    path(
        "physical_devices/",
        list_views.ListPhysicalDevicesView.as_view(),
        name="physical_devices",
    ),
    path(
        "physical_devices/detail/<pk>/",
        detail_views.DetailPhysicalDeviceView.as_view(),
        name="physical_device_detail",
    ),
    path(
        "physical_devices/create/",
        create_views.CreatePhysicalDeviceManager.as_view(),
        name="create_physical_device",
    ),
    path(
        "physical_devices/create/1/",
        create_views.SelectPhysicalDeviceDeviceTypeView.as_view(),
        name="create_physical_device_select_device_type",
    ),
    path(
        "physical_devices/create/2/",
        create_views.SelectPhysicalDeviceDeviceView.as_view(),
        name="create_physical_device_select_device",
    ),
    path(
        "physical_devices/create/3/",
        create_views.CreatePhysicalDeviceView.as_view(),
        name="create_physical_device_create_form",
    ),
]
