from irekua_database.models import Collection
from irekua_database.models import CollectionSite
from irekua_database.models import SamplingEventType

from irekua_filters.data_collections import collection_sites as site_utils
from irekua_permissions.sampling_events import (
    sampling_events as sampling_event_permissions)

from selia.views.utils import SeliaList
from selia.views.create_views.select_base import SeliaSelectView


class SelectSamplingEventSiteView(SeliaSelectView):
    template_name = 'selia/create/sampling_events/select_site.html'
    prefix = 'collection_site'
    create_url = 'selia:create_sampling_event'

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(name=self.request.GET['collection'])

    def has_view_permission(self):
        user = self.request.user
        return sampling_event_permissions.create(user, collection=self.collection)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        return context

    def get_list_class(self):
        collection_sites = CollectionSite.objects.filter(collection=self.collection)

        sampling_event_type = SamplingEventType.objects.get(
            pk=self.request.GET['sampling_event_type'])

        if sampling_event_type.restrict_site_types:
            collection_sites = collection_sites.filter(
                site_type__in=sampling_event_type.site_types.all())

        class CollectionSiteList(SeliaList):
            prefix = 'collection'

            filter_class = site_utils.Filter
            search_fields = site_utils.search_fields
            ordering_fields = site_utils.ordering_fields

            queryset = collection_sites

            list_item_template = 'selia/select_list_items/collection_sites.html'
            filter_form_template = 'selia/filters/collection_site.html'

        return CollectionSiteList
