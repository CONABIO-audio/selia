from irekua_collections.models import Collection
from irekua_collections.filters import data_collections

from selia.views.list_views.base import SeliaListView


class ListOpenCollectionsView(SeliaListView):
    template_name = "selia/list/open_collections.html"

    list_item_template = "selia/list_items/collection.html"
    help_template = "selia/help/open_collections.html"
    filter_form_template = "selia/filters/collection.html"

    filter_class = data_collections.Filter
    search_fields = data_collections.search_fields
    ordering_fields = data_collections.ordering_fields

    def has_view_permission(self):
        return True

    def get_initial_queryset(self):
        return Collection.objects.filter(is_open=True)
