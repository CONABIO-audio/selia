from selia.views.create_views.manager_base import CreateManagerBase


class CreateDeploymentManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = "selia:create_deployment"

    def view_from_request(self):
        if "collection" not in self.request.GET:
            return "selia:create_deployment_select_collection"

        if "sampling_event" not in self.request.GET:
            return "selia:create_deployment_select_sampling_event"

        if "collection_device" not in self.request.GET:
            return "selia:create_deployment_select_collection_device"

        return "selia:create_deployment_create_form"
