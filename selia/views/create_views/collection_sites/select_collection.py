from irekua_collections.filters import collections as collection_filters

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectCollectionSiteCollectionView(SeliaSelectView):
    template_name = "selia/create/collection_sites/select_collection.html"
    prefix = "collection"
    create_url = "selia:create_collection_site"

    def get_list_class(self):
        class CollectionList(SeliaList):
            filter_class = collection_filters.Filter
            search_fields = collection_filters.search_fields
            ordering_fields = collection_filters.ordering_fields

            queryset = self.request.user.collection_users.all()

            list_item_template = "selia/select_list_items/collection.html"
            filter_form_template = "selia/filters/collection.html"

        return CollectionList
