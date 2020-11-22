from selia_templates.views.manager_base import CreateManagerBase


class CreateCollectionManager(CreateManagerBase):
    manager_name = 'selia_managers:create_collection'

    def view_from_request(self):
        if 'collection_type' not in self.request.GET:
            return 'selia_managers:create_collection_select_collection_type'

        return 'selia_managers:create_collection_create_form'
