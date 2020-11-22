from django import forms

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_geo.models import Site
from irekua_geo.models import Locality
from irekua_permissions import sites as site_permissions
from selia.views.detail_views.base import SeliaDetailView


class DetailUserSiteView(SeliaDetailView):
    model = Site
    template_name = "selia/detail/site.html"

    help_template = "selia/help/user_sites.html"
    detail_template = "selia/details/site.html"
    summary_template = "selia/summaries/site.html"
    update_form_template = "selia/update/site.html"
    viewer_template = "selia/viewers/site.html"

    delete_redirect_url = "selia:user_sites"

    def get_form_class(self):
        class SiteUpdateForm(forms.ModelForm):
            class Meta:
                model = Site
                fields = ["name", "locality", "latitude", "longitude", "altitude"]

                widgets = {"locality": get_autocomplete_widget(model=Locality)}

        return SiteUpdateForm

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.view(user, site=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return site_permissions.delete(user, site=self.object)

    def has_change_permission(self):
        user = self.request.user
        return site_permissions.change(user, site=self.object)
