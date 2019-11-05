from selia.views.create_views.manager_base import CreateManagerBase


class CreatePhysicalDeviceManager(CreateManagerBase):
    manager_name = 'selia:create_physical_device'

    def view_from_request(self):
        if 'device' not in self.request.GET:
            return 'selia:create_physical_device_select_device'

        return 'selia:create_physical_device_create_form'
