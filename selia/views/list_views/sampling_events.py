from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from irekua_database.models import Collection, SamplingEvent
from selia.views.list_views.base import SeliaListView
from irekua_filters.sampling_events import sampling_events
from irekua_permissions.sampling_events import (
    sampling_events as sampling_event_permissions)
from irekua_permissions.data_collections import (
    users as user_permissions)
from irekua_permissions import (
    licences as licence_permissions)


class ListCollectionSamplingEventView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/sampling_events.html'

    list_item_template = 'selia/list_items/sampling_event.html'
    help_template = 'selia/help/collection_sampling_events.html'
    filter_form_template = 'selia/filters/collection_sampling_event.html'

    empty_message = _('No sampling events are registered in this sampling event')

    filter_class = sampling_events.Filter
    search_fields = sampling_events.search_fields
    ordering_fields = sampling_events.ordering_fields

    slug_url_kwarg = 'name'
    slug_field = 'name'

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions['list_collection_users'] = user_permissions.list(
            user, collection=self.object)
        permissions['list_collection_licences'] = licence_permissions.list(
            user, collection=self.object)
        return permissions

    def has_create_permission(self):
        user = self.request.user
        return sampling_event_permissions.create(user, collection=self.object)

    def has_view_permission(self):
        user = self.request.user
        return sampling_event_permissions.list(user, collection=self.object)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return SamplingEvent.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
