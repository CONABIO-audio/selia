from django.utils.translation import gettext as _
from django_filters import FilterSet

from irekua_collections.models import Collection
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from selia_templates.views import SeliaList
from selia_templates.views import SeliaSelectView


class Filter(FilterSet):
    class Meta:
        model = Collection
        fields = {
            'name': ['icontains'],
            'created_on': ['gt', 'lt']
        }


search_fields = (
    'name',
    'description'
)

ordering_fields = (
    ('created_on', _('created on')),
    ('name', _('name')),
)


class SelectCollectionAdministratorView(SeliaSelectView):
    template_name = 'selia_managers/create/administrator/select_collection.html'
    prefix = 'collection'
    create_url = 'selia_managers:create_administrator'

    def has_view_permission(self):
        return permissions.list(self.request.user)

    def get_list_class(self):
        user = self.request.user

        class CollectionList(SeliaList):
            filter_class = Filter
            search_fields = search_fields
            ordering_fields = ordering_fields

            if user.is_special:
                queryset = Collection.objects.all()
            else:
                queryset = user.managed_collections.all()

            list_item_template = 'selia_managers/select_list_items/collection.html'
            filter_form_template = 'selia_managers/filters/collection.html'

        return CollectionList
