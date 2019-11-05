from selia.views.create_views.manager_base import CreateManagerBase


class CreateSamplingEventManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = 'selia:create_sampling_event'

    def view_from_request(self):
        if 'collection' not in self.request.GET:
            return 'selia:create_sampling_event_select_collection'

        if 'sampling_event_type' not in self.request.GET:
            return 'selia:create_sampling_event_select_type'

        if 'collection_site' not in self.request.GET:
            return 'selia:create_sampling_event_select_site'

        return 'selia:create_sampling_event_create_form'
