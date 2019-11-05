from selia.views.create_views.manager_base import CreateManagerBase


class CreateCollectionSiteManager(CreateManagerBase):
    manager_name = 'selia:create_collection_site'

    def view_from_request(self):
        if 'collection' not in self.request.GET:
            return 'selia:create_collection_site_select_collection'

        if 'site_type' not in self.request.GET:
            return 'selia:create_collection_site_select_type'

        if 'site' not in self.request.GET:
            return 'selia:create_collection_site_select_site'

        return 'selia:create_collection_site_create_form'
