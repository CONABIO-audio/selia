from django.views.generic.detail import SingleObjectMixin
from django.db.models import Count, Max, Q, F

from irekua_collections.models import CollectionUser
from irekua_collections.models import Collection
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from irekua_filters.data_collections import collection_users
from selia_templates.views.list_base import SeliaListView


class CollectionUsersListView(SeliaListView, SingleObjectMixin):
    template_name = 'selia_managers/list/collection_user.html'
    list_item_template = 'selia_managers/list_items/collection_user.html'
    help_template = 'selia_managers/help/collection_user_list.html'
    filter_form_template = 'selia_managers/filters/collection_user.html'

    filter_class = collection_users.Filter
    search_fields = collection_users.search_fields
    ordering_fields = collection_users.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        collection = self.object
        queryset = CollectionUser.objects.filter(collection=self.object)
        queryset = queryset.annotate(
            items=Count(
                'user__item_created_by',
                filter=Q(user__item_created_by__sampling_event_device__sampling_event__collection=collection),
                distinct=True),
            annotations=Count(
                'user__annotation_created_by',
                filter=Q(user__annotation_created_by__item__sampling_event_device__sampling_event__collection=collection),
                distinct=True),
            last_item=Max(
                'user__item_created_by__created_on',
                filter=Q(user__item_created_by__sampling_event_device__sampling_event__collection=collection)),
            last_annotation=Max(
                'user__annotation_created_by__created_on',
                filter=Q(user__annotation_created_by__item__sampling_event_device__sampling_event__collection=collection)),
            is_admin=Count(
                'collection__administrators',
                filter=Q(collection__administrators=F('user')),
                distinct=True))
        return queryset

    def has_view_permission(self):
        collection_type = self.object.collection_type
        return permissions.view(self.request.user, collection_type=collection_type)

    def get_context_data(self, *args, **kwargs):
        return {
            'collection': self.object,
            **super().get_context_data(*args, **kwargs),
        }
