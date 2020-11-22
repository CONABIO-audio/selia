from django.utils.translation import gettext as _
from django.urls import reverse
from django.shortcuts import redirect
from django_filters import FilterSet

from irekua_collections.models import CollectionType
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from selia_templates.views.list_component import SeliaList
from selia_templates.views.select_base import SeliaSelectView


class Filter(FilterSet):
    class Meta:
        model = CollectionType
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


class SelectCollectionCollectionView(SeliaSelectView):
    template_name = 'selia_managers/create/collection/select_collection_type.html'
    prefix = 'collection_type'
    create_url = 'selia_managers:create_collection'

    def has_view_permission(self):
        return permissions.create(self.request.user)

    def should_redirect(self):
        self.queryset = permissions.queryset(self.request.user)
        return self.queryset.count == 1

    def handle_single_type_redirect(self):
        url = reverse('selia_managers:create_collection')

        query = self.request.GET.copy()
        query['collection_type'] = self.queryset.get().name
        full_url = '{url}?{query}'.format(
            url=url,
            query=query.urlencode())
        return redirect(full_url)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_list_class(self):
        class CollectionList(SeliaList):
            filter_class = Filter
            search_fields = search_fields
            ordering_fields = ordering_fields
            queryset = self.queryset

            list_item_template = 'selia_managers/select_list_items/collection_type.html'
            filter_form_template = 'selia_managers/filters/collection_type.html'

        return CollectionList
