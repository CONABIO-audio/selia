from irekua_collections.models import SamplingEvent
from irekua_collections.models import CollectionDevice

from irekua_collections.filters import collection_devices as device_filters
from irekua_permissions.sampling_events import devices as device_permissions

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectDeploymentCollectionDeviceView(SeliaSelectView):
    template_name = "selia/create/deployments/select_collection_device.html"
    prefix = "collection_device"
    create_url = "selia:create_deployment"

    def get_objects(self):
        if not hasattr(self, "sampling_event"):
            self.sampling_event = SamplingEvent.objects.get(
                pk=self.request.GET["sampling_event"]
            )

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.create(user, sampling_event=self.sampling_event)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["sampling_event"] = self.sampling_event
        context["collection"] = self.sampling_event.collection
        return context

    def get_list_class(self):
        collection_pk = self.request.GET["collection"]

        sampling_event_type = self.sampling_event.sampling_event_type
        device_types = sampling_event_type.device_types.all()

        collection_devices = CollectionDevice.objects.filter(
            collection__name=collection_pk
        ).exclude(samplingeventdevice__sampling_event=self.sampling_event)

        if sampling_event_type.restrict_device_types:
            collection_devices = collection_devices.filter(
                physical_device__device__device_type__in=device_types
            )

        class CollectionDeviceList(SeliaList):
            filter_class = device_filters.Filter
            search_fields = device_filters.search_fields
            ordering_fields = device_filters.ordering_fields

            queryset = collection_devices

            list_item_template = "selia/select_list_items/collection_devices.html"
            filter_form_template = "selia/filters/collection_device.html"

        return CollectionDeviceList
