from django import forms

from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField
from irekua_permissions.sampling_events import (
    devices as device_permissions)
from irekua_database.models import SamplingEventDevice
from irekua_database.models import SamplingEventTypeDeviceType


class SamplingEventDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()
    configuration = JsonField()

    class Meta:
        model = SamplingEventDevice
        fields = [
            'metadata',
            'commentaries',
            'configuration',
        ]


class DetailSamplingEventDeviceView(SeliaDetailView):
    model = SamplingEventDevice
    form_class = SamplingEventDeviceUpdateForm
    delete_redirect_url = 'selia:user_physical_devices'

    template_name = 'selia/detail/sampling_event_device.html'
    help_template = 'selia/components/help/sampling_event_device_detail.html'
    summary_template = 'selia/components/summaries/sampling_event_device.html'
    detail_template = 'selia/components/details/sampling_event_device.html'
    update_form_template = 'selia/components/update/sampling_event_device.html'

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.view(user, sampling_event_device=self.object)

    def has_change_permission(self):
        user = self.request.user
        return device_permissions.change(user, sampling_event_device=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return device_permissions.delete(user, sampling_event_device=self.object)

    def get_delete_redirect_url_args(self):
        return [self.object.sampling_event.pk]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sampling_event_device = self.object
        sampling_event = sampling_event_device.sampling_event
        sampling_event_type = sampling_event.sampling_event_type
        collection_device = sampling_event_device.collection_device
        device = collection_device.physical_device.device

        context['sampling_event_device'] = sampling_event_device
        context['device'] = device

        if sampling_event_type.restrict_device_types:
            info = SamplingEventTypeDeviceType.objects.get(
                    sampling_event_type=sampling_event_type,
                    device_type=device.device_type)

            context['info'] = info
            context['form'].fields['metadata'].update_schema(
                info.metadata_schema)
            context['form'].fields['configuration'].update_schema(
                device.configuration_schema)

        return context
