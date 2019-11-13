from irekua_filters.data_collections import data_collections as collection_utils

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectItemCollectionView(SeliaSelectView):
    template_name = 'selia/create/items/select_collection.html'
    prefix = 'collection'
    create_url = 'selia:create_item'

    def get_list_class(self):
        class CollectionList(SeliaList):
            filter_class = collection_utils.Filter
            search_fields = collection_utils.search_fields
            ordering_fields = collection_utils.ordering_fields

            queryset = self.request.user.collection_users.all()

            list_item_template = 'selia/select_list_items/user_collections.html'
            filter_form_template = 'selia/filters/collection.html'

        return CollectionList
