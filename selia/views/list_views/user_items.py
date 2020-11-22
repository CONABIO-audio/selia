from django.utils.translation import gettext as _

from irekua_items.models import Item
from irekua_items.filters import items

from selia.views.list_views.base import SeliaListView


class ListUserItemsView(SeliaListView):
    template_name = "selia/list/user_items.html"

    list_item_template = "selia/list_items/item.html"
    help_template = "selia/help/user_items.html"
    filter_form_template = "selia/filters/item.html"

    empty_message = _("User has no registered items")

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def get_initial_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
