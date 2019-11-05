from selia.views.create_views.manager_base import CreateManagerBase


class CreateSamplingEventDeviceManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = 'selia:create_sampling_event_device'

    def view_from_request(self):
        if 'collection' not in self.request.GET:
            return 'selia:create_sampling_event_device_select_collection'

        if 'sampling_event' not in self.request.GET:
            return 'selia:create_sampling_event_device_select_sampling_event'

        if 'collection_device' not in self.request.GET:
            return 'selia:create_sampling_event_device_select_collection_device'

        return 'selia:create_sampling_event_device_create_form'
