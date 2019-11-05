from django import forms

from irekua_database.models import PhysicalDevice
from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField
from irekua_permissions.devices import (
    physical_devices as device_permissions)


class PhysicalDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            'identifier',
            'serial_number',
        ]


class DetailPhysicalDeviceView(SeliaDetailView):
    model = PhysicalDevice
    form_class = PhysicalDeviceUpdateForm
    delete_redirect_url = 'selia:user_physical_devices'

    template_name = 'selia/detail/physical_device.html'
    help_template = 'selia/components/help/physical_device.html'
    detail_template = 'selia/components/details/physical_device.html'
    summary_template = 'selia/components/summaries/physical_device.html'
    update_form_template = 'selia/components/update/physical_device.html'

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.view(user, physical_device=self.object)

    def has_change_permission(self):
        user = self.request.user
        return device_permissions.change(user, physical_device=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return device_permissions.delete(user, physical_device=self.object)
