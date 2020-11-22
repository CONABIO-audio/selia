from selia_templates.views import CreateManagerBase


class CreatePhysicalDeviceManager(CreateManagerBase):
    manager_name = "selia_user_home:create_physical_device"

    def view_from_request(self):
        if "device_type" not in self.request.GET:
            return "selia_user_home:create_physical_device_select_device_type"

        if "device" not in self.request.GET:
            return "selia_user_home:create_physical_device_select_device"

        return "selia_user_home:create_physical_device_create_form"
