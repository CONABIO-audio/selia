from irekua_database.models import Collection
from irekua_filters.data_collections import data_collections as collection_utils
from selia.views.utils import SeliaList
from selia.views.create_views.select_base import SeliaSelectView


class SelectSamplingEventCollectionView(SeliaSelectView):
    template_name = 'selia/create/sampling_events/select_collection.html'
    prefix = 'collection'
    create_url = 'selia:create_sampling_event'

    def get_list_class(self):
        class CollectionList(SeliaList):
            prefix = 'collection'

            filter_class = collection_utils.Filter
            search_fields = collection_utils.search_fields
            ordering_fields = collection_utils.ordering_fields

            queryset = Collection.objects.all()

            list_item_template = 'selia/select_list_items/user_collections.html'
            filter_form_template = 'selia/filters/collection.html'

        return CollectionList
