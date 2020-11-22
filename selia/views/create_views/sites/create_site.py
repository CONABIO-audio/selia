from django.forms import ModelForm

from irekua_database.autocomplete import get_autocomplete_widget
from selia.views.create_views.create_base import SeliaCreateView
from irekua_geo.models import Site
from irekua_geo.models import Locality
from irekua_permissions import sites as site_permissions


class CreateSiteView(SeliaCreateView):
    template_name = "selia/create/sites/create_form.html"
    success_url = "selia:user_sites"

    def get_form_class(self):
        class SiteForm(ModelForm):
            class Meta:
                model = Site
                fields = [
                    "latitude",
                    "longitude",
                    "altitude",
                    "name",
                    "locality",
                    "geo_ref",
                ]

                widgets = {"locality": get_autocomplete_widget(model=Locality)}

        return SiteForm

    def form_invalid(self, form):
        if "locality" in form.data:
            try:
                self.locality = Locality.objects.get(pk=form.data["locality"])
            except Locality.DoesNotExists:
                pass
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self, "locality"):
            context["locality"] = self.locality

        return context

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user)

    def get_additional_query_on_sucess(self):
        return {
            "site": self.object.pk,
        }
