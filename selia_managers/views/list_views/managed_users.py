from django.db.models import Count, Max

from irekua_database.models import User
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from irekua_filters.users import users
from selia_templates.views.list_base import SeliaListView


class ManagedUsersListView(SeliaListView):
    template_name = 'selia_managers/list/managed_user.html'
    list_item_template = 'selia_managers/list_items/managed_user.html'
    help_template = 'selia_managers/help/managed_user_list.html'
    filter_form_template = 'selia_managers/filters/managed_user.html'

    filter_class = users.Filter
    search_fields = users.search_fields
    ordering_fields = users.ordering_fields

    def get_initial_queryset(self):
        user = self.request.user

        if user.is_special:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(
                collection_users__collection_type__administrators=user).distinct()

        queryset = queryset.annotate(
            collection_users_count=Count('collection_users', distinct=True),
            collection_administrators_count=Count('collection_administrators', distinct=True),
            items=Count('item_created_by', distinct=True),
            annotations=Count('annotation_created_by', distinct=True),
            last_item=Max('item_created_by__created_on'),
            last_annotation=Max('annotation_created_by__created_on'),
        )

        return queryset

    def has_view_permission(self):
        return permissions.list(self.request.user)
