from selia.views.create_views.manager_base import CreateManagerBase


class CreateLicenceManager(CreateManagerBase):
    required_get_parameters = ['collection']
    manager_name = 'selia:create_licence'

    def view_from_request(self):
        if 'licence_type' not in self.request.GET:
            return 'selia:create_licence_select_type'

        return 'selia:create_licence_create_form'
