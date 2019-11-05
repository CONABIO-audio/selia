from irekua_database.models import Collection
from irekua_filters.data_collections import data_collections as collection_utils
from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectSamplingEventDeviceCollectionView(SeliaSelectView):
    template_name = 'selia/create/sampling_event_devices/select_collection.html'
    prefix = 'collection'
    create_url = 'selia:create_sampling_event_device'

    def get_list_class(self):
        class CollectionList(SeliaList):
            filter_class = collection_utils.Filter
            search_fields = collection_utils.search_fields
            ordering_fields = collection_utils.ordering_fields

            queryset = Collection.objects.all()

            list_item_template = 'selia/components/select_list_items/user_collections.html'
            filter_form_template = 'selia/components/filters/collection.html'

        return CollectionList
