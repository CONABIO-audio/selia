from django.utils.translation import gettext as _

from irekua_geo.models import Site
from irekua_geo.filters import sites
from selia_templates.views import SeliaListView


class ListSitesView(SeliaListView):
    template_name = "selia_user_home/list/sites.html"
    list_item_template = "selia_user_home/list_items/sites.html"
    help_template = "selia_user_home/help/sites_list.html"
    filter_form_template = "selia_user_home/filters/sites.html"

    empty_message = _("User has no registered sites")

    filter_class = sites.Filter
    search_fields = sites.search_fields
    ordering_fields = zip(sites.ordering_fields, sites.ordering_fields)

    def get_initial_queryset(self):
        return Site.objects.filter(created_by=self.request.user)

    def has_view_permission(self):
        user = self.request.user
        return user.is_authenticated

    def has_create_permission(self):
        user = self.request.user
        return user.is_authenticated
