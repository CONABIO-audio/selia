from irekua_database.models import Collection

from irekua_filters.devices import physical_devices as device_utils
from irekua_permissions.data_collections import (
    devices as device_permissions)

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectCollectionDevicePhysicalDeviceView(SeliaSelectView):
    template_name = 'selia/create/collection_devices/select_device.html'
    prefix = 'physical_device'
    create_url = 'selia:create_collection_device'

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.create(user, collection=self.collection)

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                name=self.request.GET['collection'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        context['collection'] = self.collection
        return context

    def get_list_class(self):
        devices = self.request.user.physicaldevice_created_by.exclude(
            collectiondevice__collection__name=self.request.GET['collection'])

        collection_type = self.collection.collection_type

        if collection_type.restrict_device_types:
            devices = devices.filter(
                device__device_type__in=collection_type.device_types.all())

        class DeviceList(SeliaList):
            filter_class = device_utils.Filter
            search_fields = device_utils.search_fields
            ordering_fields = device_utils.ordering_fields

            queryset = devices

            list_item_template = 'selia/select_list_items/physical_devices.html'
            filter_form_template = 'selia/filters/physical_device.html'

        return DeviceList
