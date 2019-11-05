from selia.views.create_views.manager_base import CreateManagerBase


class CreateSiteManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = 'selia:create_site'

    def view_from_request(self):
        return 'selia:create_site_create_form'
