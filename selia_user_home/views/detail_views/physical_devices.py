from django import forms

from irekua_devices.models import PhysicalDevice
from selia_templates.views import SeliaDetailView
from selia_templates.forms.json_field import JsonField


class PhysicalDeviceUpdateForm(forms.ModelForm):
    device_metadata = JsonField()
    device_type_metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            "name",
            "serial_number",
            "device_type_metadata",
            "device_metadata",
        ]


class DetailPhysicalDeviceView(SeliaDetailView):
    model = PhysicalDevice
    form_class = PhysicalDeviceUpdateForm
    delete_redirect_url = "selia_user_home:physical_devices"
    template_name = "selia_user_home/detail/physical_devices.html"
    help_template = "selia_user_home/help/physical_devices_detail.html"
    detail_template = "selia_user_home/details/physical_devices.html"
    summary_template = "selia_user_home/summaries/physical_devices.html"
    update_form_template = "selia_user_home/update/physical_devices.html"

    def user_owns_object(self):
        user = self.request.user
        return self.object.created_by == user

    # pylint: disable=signature-differs
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["device_metadata"].update_schema(
            self.object.device.metadata_schema,
        )
        form.fields["device_type_metadata"].update_schema(
            self.object.device.device_type.metadata_schema,
        )
        return form

    def has_view_permission(self):
        return self.user_owns_object()

    def has_change_permission(self):
        return self.user_owns_object()

    def has_delete_permission(self):
        return self.user_owns_object()
