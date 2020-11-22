from selia.views.create_views.manager_base import CreateManagerBase


class CreateUserManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = 'selia:create_user'

    def view_from_request(self):
        return 'selia:create_user_create_form'
