from django.utils.translation import gettext as _

from irekua_collections.models import SamplingEvent
from irekua_collections.filters import sampling_events

from selia.views.list_views.base import SeliaListView


class ListUserSamplingEventsView(SeliaListView):
    template_name = "selia/list/user_sampling_events.html"

    list_item_template = "selia/list_items/sampling_event.html"
    help_template = "selia/help/user_sampling_events.html"
    filter_form_template = "selia/filters/sampling_event.html"

    empty_message = _("User has no registered sampling events")

    filter_class = sampling_events.Filter
    search_fields = sampling_events.search_fields
    ordering_fields = sampling_events.ordering_fields

    def get_initial_queryset(self):
        return SamplingEvent.objects.filter(created_by=self.request.user)
