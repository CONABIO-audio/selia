from irekua_filters.data_collections import data_collections as collection_utils

from irekua_database.models import Collection
from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectCollectionUserCollectionView(SeliaSelectView):
    template_name = 'selia/create/collection_users/select_collection.html'
    prefix = 'collection'
    create_url = 'selia:create_collection_user'

    def get_list_class(self):
        class CollectionList(SeliaList):
            filter_class = collection_utils.Filter
            search_fields = collection_utils.search_fields
            ordering_fields = collection_utils.ordering_fields

            queryset = Collection.objects.filter(administrators=self.request.user)

            list_item_template = 'selia/select_list_items/collection.html'
            filter_form_template = 'selia/filters/collection.html'

        return CollectionList
