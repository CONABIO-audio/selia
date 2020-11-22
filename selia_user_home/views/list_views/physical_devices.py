from django.utils.translation import gettext as _

from irekua_devices.filters import physical_devices
from irekua_devices.models import PhysicalDevice
from selia_templates.views import SeliaListView


class ListPhysicalDevicesView(SeliaListView):
    template_name = "selia_user_home/list/physical_devices.html"
    list_item_template = "selia_user_home/list_items/physical_devices.html"
    help_template = "selia_user_home/help/physical_devices_list.html"
    filter_form_template = "selia_user_home/filters/physical_devices.html"

    empty_message = _("User has no registered devices")

    filter_class = physical_devices.Filter
    search_fields = physical_devices.search_fields
    ordering_fields = zip(
        physical_devices.ordering_fields, physical_devices.ordering_fields
    )

    def get_initial_queryset(self):
        return PhysicalDevice.objects.filter(created_by=self.request.user)
