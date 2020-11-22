from django.views.generic.detail import SingleObjectMixin

from irekua_collections.models import Collection
from irekua_collections.models import CollectionLicence
from irekua_collections.filters import collection_licences

from irekua_permissions import licences as licence_permissions
from irekua_permissions.data_collections import users as user_permissions

from selia.views.list_views.base import SeliaListView


class ListCollectionLicencesView(SeliaListView, SingleObjectMixin):
    template_name = "selia/list/collection_licences.html"

    list_item_template = "selia/list_items/licence.html"
    help_template = "selia/help/collection_licences.html"
    filter_form_template = "selia/filters/licence.html"
    viewer_template = "selia/viewers/licence.html"

    filter_class = collection_licences.Filter
    search_fields = collection_licences.search_fields
    ordering_fields = collection_licences.ordering_fields

    slug_url_kwarg = "name"
    slug_field = "name"

    def has_view_permission(self):
        user = self.request.user
        return licence_permissions.list(user, collection=self.object)

    def has_create_permission(self):
        user = self.request.user
        return licence_permissions.create(user, collection=self.object)

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions["list_collection_users"] = user_permissions.list(
            user, collection=self.object
        )
        permissions["list_collection_licences"] = licence_permissions.list(
            user, collection=self.object
        )
        return permissions

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return CollectionLicence.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["collection"] = self.object
        return context
