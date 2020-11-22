from django import forms

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_permissions import sites as site_permissions
from irekua_geo.models import Site
from irekua_geo.models import Locality
from selia_templates.views import SeliaDetailView


class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "locality"]
        widgets = {"locality": get_autocomplete_widget(model=Locality)}


class DetailSiteView(SeliaDetailView):
    model = Site
    form_class = SiteUpdateForm
    delete_redirect_url = "selia_user_home:sites"
    template_name = "selia_user_home/detail/sites.html"
    help_template = "selia_user_home/help/sites_detail.html"
    detail_template = "selia_user_home/details/sites.html"
    summary_template = "selia_user_home/summaries/sites.html"
    update_form_template = "selia_user_home/update/sites.html"
    viewer_template = "selia_user_home/viewers/sites.html"

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.view(user, site=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return site_permissions.delete(user, site=self.object)

    def has_change_permission(self):
        user = self.request.user
        return site_permissions.change(user, site=self.object)
