from django.utils.translation import gettext as _

from irekua_items.models import Item
from irekua_items.filters import items
from selia_templates.views import SeliaListView


class ListItemsView(SeliaListView):
    template_name = "selia_user_home/list/items.html"
    list_item_template = "selia_user_home/list_items/items.html"
    help_template = "selia_user_home/help/items_list.html"
    filter_form_template = "selia_user_home/filters/items.html"

    empty_message = _("User has no registered items")

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = zip(items.ordering_fields, items.ordering_fields)

    def get_initial_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
