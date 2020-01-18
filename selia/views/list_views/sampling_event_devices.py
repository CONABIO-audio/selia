from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from irekua_database.models import SamplingEvent, SamplingEventDevice
from irekua_filters.sampling_events import sampling_event_devices
from irekua_permissions.sampling_events import devices as device_permissions
from selia.views.list_views.base import SeliaListView


class ListSamplingEventDevicesView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/sampling_event_devices.html'

    list_item_template = 'selia/list_items/sampling_event_device.html'
    help_template = 'selia/help/sampling_event_device.html'
    filter_form_template = 'selia/filters/sampling_event_device.html'

    empty_message = _('No devices are registered in this sampling event')

    filter_class = sampling_event_devices.Filter
    search_fields = sampling_event_devices.search_fields
    ordering_fields = sampling_event_devices.ordering_fields

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.list(user, sampling_event=self.object)

    def has_create_permission(self):
        user = self.request.user
        return device_permissions.create(user, sampling_event=self.object)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SamplingEvent.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return SamplingEventDevice.objects.filter(sampling_event=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = self.object
        context['collection'] = self.object.collection
        return context
