from django import forms

from irekua_devices.models import Device
from irekua_devices.models import DeviceType
from irekua_devices.models import PhysicalDevice
from selia_templates.forms.json_field import JsonField
from selia_templates.views import SeliaCreateView


class PhysicalDeviceCreateForm(forms.ModelForm):
    device_metadata = JsonField()
    device_type_metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            "device",
            "name",
            "serial_number",
            "device_metadata",
            "device_type_metadata",
        ]


class CreatePhysicalDeviceView(SeliaCreateView):
    model = PhysicalDevice
    form_class = PhysicalDeviceCreateForm
    template_name = "selia_user_home/create/physical_devices/create_form.html"
    success_url = "selia_user_home:physical_devices"

    def get_objects(self):
        if not hasattr(self, "device"):
            self.device = Device.objects.get(pk=self.request.GET["device"])

        if not hasattr(self, "device_type"):
            self.device_type = DeviceType.objects.get(
                pk=self.request.GET["device_type"]
            )

    def get_success_url_args(self):
        return []

    def get_initial(self):
        return {"device": self.device}

    def get_additional_query_on_sucess(self):
        return {"physical_device": self.object.pk}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["device"] = self.device
        context["device_type"] = self.device_type
        context["form"].fields["device_metadata"].update_schema(
            self.device.metadata_schema
        )
        context["form"].fields["device_type_metadata"].update_schema(
            self.device.device_type.metadata_schema
        )
        return context
