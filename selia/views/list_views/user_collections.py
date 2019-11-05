from irekua_database.models import Collection

from selia.views.list_views.base import SeliaListView
from irekua_filters.data_collections import data_collections


class ListUserCollectionsView(SeliaListView):
    template_name = 'selia/list/user_collections.html'

    list_item_template = 'selia/components/list_items/collection.html'
    help_template = 'selia/components/help/user_collections.html'
    filter_form_template = 'selia/components/filters/collection.html'

    filter_class = data_collections.Filter
    search_fields = data_collections.search_fields
    ordering_fields = data_collections.ordering_fields

    def get_initial_queryset(self):
        user = self.request.user
        queryset = user.collection_users.all()

        if user.collection_administrators.exists():
            queryset = queryset.union(user.collection_administrators.all())

        if user.collectiontype_set.exists():
            managed_collections = Collection.objects.filter(
                collection_type__in=user.collectiontype_set.all())
            queryset = queryset.union(managed_collections)

        return queryset

    def has_view_permission(self):
        return self.request.user.is_authenticated
