from django.views.generic.detail import SingleObjectMixin

from irekua_database.models import Collection
from irekua_database.models import CollectionSite

from selia.views.list_views.base import SeliaListView
from irekua_permissions.data_collections import (
    sites as site_permissions)
from irekua_permissions.data_collections import (
    users as user_permissions)
from irekua_permissions import (
    licences as licence_permissions)
from irekua_filters.data_collections import collection_sites


class ListCollectionSitesView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/collection_sites.html'

    list_item_template = 'selia/components/list_items/collection_site.html'
    help_template = 'selia/components/help/collection_sites.html'
    filter_form_template = 'selia/components/filters/collection_site.html'

    filter_class = collection_sites.Filter
    search_fields = collection_sites.search_fields
    ordering_fields = collection_sites.ordering_fields

    def has_create_permission(self):
        user = self.request.user
        return site_permissions.create(user, collection=self.object)

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions['list_collection_users'] = user_permissions.list(
            user, collection=self.object)
        permissions['list_collection_licences'] = licence_permissions.list(
            user, collection=self.object)
        return permissions


    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return CollectionSite.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
