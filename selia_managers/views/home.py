from django.contrib.auth.mixins import LoginRequiredMixin
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from selia_templates.views import SeliaListView


class CollectionManagementHome(LoginRequiredMixin, SeliaListView):
    template_name = 'selia_managers/home.html'
    list_item_template = 'selia_managers/list_items/collection_type_brief.html'
    help_template = 'selia_managers/help/home.html'
    filter_form_template = 'selia_managers/filters/collection_type.html'

    def get_initial_queryset(self):
        return permissions.queryset(self.request.user)

    def has_view_permission(self):
        return permissions.list(self.request.user)
