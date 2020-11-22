from django.db.models import Count, Max
from django_filters import FilterSet

from irekua_collections.models import Collection
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from irekua_filters.data_collections import data_collections
from selia_templates.views.list_base import SeliaListView


class ManagedCollectionFilter(FilterSet):
    class Meta:
        model = Collection
        fields = {
            'collection_type': ['exact'],
            'name': ['icontains'],
            'institution': ['exact'],
            'institution__institution_name': ['exact', 'icontains'],
            'institution__institution_code': ['exact', 'icontains'],
            'institution__country': ['icontains'],
            'created_on': ['gt', 'lt'],
            'administrators': ['exact'],
            'administrators__username': ['icontains'],
            'administrators__first_name': ['icontains'],
            'administrators__last_name': ['icontains'],
            'administrators__email': ['icontains'],
            'users': ['exact'],
            'users__username': ['icontains'],
            'users__first_name': ['icontains'],
            'users__last_name': ['icontains'],
            'users__email': ['icontains'],
        }


class ManagedCollectionsListView(SeliaListView):
    template_name = 'selia_managers/list/managed_collections.html'
    list_item_template = 'selia_managers/list_items/managed_collection.html'
    help_template = 'selia_managers/help/managed_collections.html'
    filter_form_template = 'selia_managers/filters/managed_collections.html'

    filter_class = ManagedCollectionFilter
    search_fields = data_collections.search_fields
    ordering_fields = data_collections.ordering_fields

    def get_initial_queryset(self):
        user = self.request.user

        if user.is_special:
            queryset = Collection.objects.all()
        else:
            queryset = Collection.objects.filter(
                collection_type__administrators=user
            )

        return queryset.annotate(
            user_count=Count('users', distinct=True),
            admin_count=Count('administrators', distinct=True),
            item_count=Count('samplingevent__samplingeventdevice__item', distinct=True),
            annotation_count=Count('samplingevent__samplingeventdevice__item__annotation', distinct=True),
            last_item=Max('samplingevent__samplingeventdevice__item__created_on'),
            last_annotation=Max('samplingevent__samplingeventdevice__item__annotation__created_on'))

    def has_view_permission(self):
        return permissions.list(self.request.user)

    def has_create_permission(self):
        return permissions.create(self.request.user)
