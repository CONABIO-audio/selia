from django.utils.translation import gettext as _

from irekua_database.models import Site

from irekua_filters import sites
from irekua_permissions import sites as site_permissions
from selia.views.list_views.base import SeliaListView


class ListUserSitesView(SeliaListView):
    template_name = 'selia/list/user_sites.html'

    list_item_template = 'selia/list_items/site.html'
    help_template = 'selia/help/user_sites.html'
    filter_form_template = 'selia/filters/site.html'

    empty_message = _('User has no registered sites')

    filter_class = sites.Filter
    search_fields = sites.search_fields
    ordering_fields = sites.ordering_fields

    def get_initial_queryset(self):
        return Site.objects.filter(created_by=self.request.user)

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user)

    def has_create_permission(self):
        user = self.request.user
        return site_permissions.create(user)
