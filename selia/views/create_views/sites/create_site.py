from django.forms import ModelForm

from irekua_autocomplete.utils import get_autocomplete_widget
from selia.views.create_views.create_base import SeliaCreateView
from irekua_database.models import Site
from irekua_permissions import sites as site_permissions


class CreateSiteView(SeliaCreateView):
    template_name = 'selia/create/sites/create_form.html'
    success_url = 'selia:user_sites'

    def get_form_class(self):
        class SiteForm(ModelForm):
            class Meta:
                model = Site
                fields = [
                    'latitude',
                    'longitude',
                    'altitude',
                    'name',
                    'locality',
                ]

                widgets = {
                    'locality': get_autocomplete_widget(name='localities')
                }

        return SiteForm

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user)

    def get_additional_query_on_sucess(self):
        return {
            'site': self.object.pk,
        }
