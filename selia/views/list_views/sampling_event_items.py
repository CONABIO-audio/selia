from irekua_database.models import SamplingEvent
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from irekua_database.models import Item

from irekua_filters.items import items
from irekua_permissions.items import (
    items as item_permissions)
from selia.views.list_views.base import SeliaListView


class ListSamplingEventItemsView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/sampling_event_items.html'

    list_item_template = 'selia/list_items/item.html'
    help_template = 'selia/help/sampling_event_items.html'
    filter_form_template = 'selia/filters/item.html'

    empty_message = _('No items are registered in this sampling event')

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.list(user, sampling_event=self.object)

    def has_create_permission(self):
        user = self.request.user
        return item_permissions.create(user, sampling_event=self.object)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SamplingEvent.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = self.object
        context['collection'] = self.object.collection
        return context
