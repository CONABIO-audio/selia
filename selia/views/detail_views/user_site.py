from django import forms

from irekua_database.models import Site
from selia.views.detail_views.base import SeliaDetailView
from irekua_permissions import sites as site_permissions


class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name',
            'locality',
            'latitude',
            'longitude',
            'altitude'
        ]


class DetailUserSiteView(SeliaDetailView):
    model = Site
    form_class = SiteUpdateForm

    template_name = 'selia/detail/site.html'

    help_template = 'selia/components/help/user_sites.html'
    detail_template = 'selia/components/details/site.html'
    summary_template = 'selia/components/summaries/site.html'
    update_form_template = 'selia/components/update/site.html'
    viewer_template = 'selia/components/viewers/site.html'

    delete_redirect_url = 'selia:user_sites'

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.view(user, site=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return site_permissions.delete(user, site=self.object)

    def has_change_permission(self):
        user = self.request.user
        return site_permissions.change(user, site=self.object)
