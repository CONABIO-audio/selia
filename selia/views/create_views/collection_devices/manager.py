from selia.views.create_views.manager_base import CreateManagerBase


class CreateCollectionDeviceManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = 'selia:create_collection_device'

    def view_from_request(self):
        if 'collection' not in self.request.GET:
            return 'selia:create_collection_device_select_collection'

        if 'physical_device' not in self.request.GET:
            return 'selia:create_collection_device_select_device'

        return 'selia:create_collection_device_create_form'
