from irekua_collections.models import SamplingEvent
from irekua_collections.models import Collection

from irekua_collections.filters import sampling_events as sampling_event_filters
from irekua_permissions.items import items as item_permissions

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectItemSamplingEventView(SeliaSelectView):
    template_name = "selia/create/items/select_sampling_event.html"
    prefix = "sampling_event"
    create_url = "selia:create_item"

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.create(user, collection=self.collection)

    def get_objects(self):
        if not hasattr(self, "collection"):
            self.collection = Collection.objects.get(
                name=self.request.GET["collection"]
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["collection"] = self.collection
        return context

    def get_queryset(self):
        queryset = SamplingEvent.objects.filter(
            collection__name=self.request.GET["collection"]
        )

        if "collection_device" in self.request.GET:
            collection_device_pk = self.request.GET["collection_device"]
            queryset = queryset.filter(
                samplingeventdevice__collection_device=collection_device_pk
            )

        return queryset

    def get_list_class(self):
        class SamplingEventList(SeliaList):
            filter_class = sampling_event_filters.Filter
            search_fields = sampling_event_filters.search_fields
            ordering_fields = sampling_event_filters.ordering_fields

            queryset = self.get_queryset()

            list_item_template = "selia/select_list_items/sampling_events.html"
            filter_form_template = "selia/filters/sampling_event.html"

        return SamplingEventList
