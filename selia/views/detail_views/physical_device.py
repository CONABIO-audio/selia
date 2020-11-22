from django import forms

from irekua_devices.models import PhysicalDevice
from selia.views.detail_views.base import SeliaDetailView
from selia_templates.forms.json_field import JsonField
from irekua_permissions.devices import (
    physical_devices as device_permissions)


class PhysicalDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            'name',
            'serial_number',
        ]


class DetailPhysicalDeviceView(SeliaDetailView):
    model = PhysicalDevice
    form_class = PhysicalDeviceUpdateForm
    delete_redirect_url = 'selia:user_physical_devices'

    template_name = 'selia/detail/physical_device.html'
    help_template = 'selia/help/physical_device.html'
    detail_template = 'selia/details/physical_device.html'
    summary_template = 'selia/summaries/physical_device.html'
    update_form_template = 'selia/update/physical_device.html'

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.view(user, physical_device=self.object)

    def has_change_permission(self):
        user = self.request.user
        return device_permissions.change(user, physical_device=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return device_permissions.delete(user, physical_device=self.object)
