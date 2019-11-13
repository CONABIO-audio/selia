from irekua_database.models import SamplingEventDevice
from irekua_database.models import SamplingEvent

from irekua_filters.sampling_events import sampling_event_devices as sampling_event_utils
from irekua_permissions.items import (
    items as item_permissions)

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectItemSamplingEventDeviceView(SeliaSelectView):
    template_name = 'selia/create/items/select_sampling_event_device.html'
    prefix = 'sampling_event_device'
    create_url = 'selia:create_item'

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.create(user, sampling_event=self.sampling_event)

    def get_objects(self):
        if not hasattr(self, 'sampling_event'):
            self.sampling_event = SamplingEvent.objects.get(
                pk=self.request.GET['sampling_event'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = self.sampling_event
        return context

    def get_list_class(self):
        sampling_event = self.request.GET['sampling_event']

        class SamplingEventDeviceList(SeliaList):
            filter_class = sampling_event_utils.Filter
            search_fields = sampling_event_utils.search_fields
            ordering_fields = sampling_event_utils.ordering_fields

            queryset = SamplingEventDevice.objects.filter(sampling_event__pk=sampling_event)

            list_item_template = 'selia/select_list_items/sampling_event_devices.html'
            filter_form_template = 'selia/filters/sampling_event_device.html'

        return SamplingEventDeviceList
