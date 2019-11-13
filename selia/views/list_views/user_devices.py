from django.utils.translation import gettext as _

from irekua_database.models import PhysicalDevice

from irekua_filters.devices import physical_devices
from selia.views.list_views.base import SeliaListView


class ListUserPhysicalDeviceView(SeliaListView):
    template_name = 'selia/list/user_physical_devices.html'

    list_item_template = 'selia/list_items/physical_device.html'
    help_template = 'selia/help/user_devices.html'
    filter_form_template = 'selia/filters/physical_device.html'

    empty_message = _('User has no registered devices')

    filter_class = physical_devices.Filter
    search_fields = physical_devices.search_fields
    ordering_fields = physical_devices.ordering_fields

    def get_initial_queryset(self):
        return PhysicalDevice.objects.filter(created_by=self.request.user)
