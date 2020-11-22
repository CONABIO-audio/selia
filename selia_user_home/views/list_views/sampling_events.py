from django.utils.translation import gettext as _

from irekua_collections.models import SamplingEvent
from irekua_collections.filters import sampling_events
from selia_templates.views import SeliaListView


class ListSamplingEventsView(SeliaListView):
    template_name = "selia_user_home/list/sampling_events.html"
    list_item_template = "selia_user_home/list_items/sampling_events.html"
    help_template = "selia_user_home/help/sampling_events_list.html"
    filter_form_template = "selia_user_home/filters/sampling_events.html"

    empty_message = _("User has no registered sampling events")

    filter_class = sampling_events.Filter
    search_fields = sampling_events.search_fields
    ordering_fields = zip(
        sampling_events.ordering_fields, sampling_events.ordering_fields
    )

    def get_initial_queryset(self):
        return SamplingEvent.objects.filter(created_by=self.request.user)
