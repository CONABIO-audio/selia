from selia.views.create_views.manager_base import CreateManagerBase


class CreateItemManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = "selia:create_item"

    def view_from_request(self):
        if "collection" not in self.request.GET:
            return "selia:create_item_select_collection"

        if "sampling_event" not in self.request.GET:
            return "selia:create_item_select_sampling_event"

        if "licence" not in self.request.GET:
            return "selia:create_item_select_licence"

        if "item_type" not in self.request.GET:
            return "selia:create_item_select_item_type"

        return "selia_uploader:upload_app"
