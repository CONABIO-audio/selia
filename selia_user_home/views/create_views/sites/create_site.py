from django.contrib.gis import forms
from django.http import Http404

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_geo.models import Site
from irekua_geo.models import get_site_class
from irekua_geo.models import Locality
from selia_templates.views import SeliaCreateView


class BaseSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            "name",
            "locality",
        ]
        widgets = {"locality": get_autocomplete_widget(model=Locality)}

    def save(self, commit=True):
        # Get geometry from form
        geometry = self.cleaned_data["geometry"]
        geometry_type = geometry.geom_type
        self.cleaned_data["geometry_type"] = geometry_type

        # Add geometry to the extended model
        site_class = get_site_class(geometry_type)
        geom_site = site_class(**self.cleaned_data)
        geom_site.save()
        return geom_site.site_ptr


class CreateSiteView(SeliaCreateView):
    template_name = "selia_user_home/create/sites/create_form.html"
    success_url = "selia_user_home:sites"

    def get_form_class(self):
        class SiteForm(BaseSiteForm):
            geometry = self.get_geometry_field()

        return SiteForm

    def get_geometry_field(self):
        geometry_type = self.request.GET["geometry_type"]

        if geometry_type == Site.POINT:
            return forms.PointField()

        if geometry_type == Site.LINESTRING:
            return forms.LineStringField()

        if geometry_type == Site.POLYGON:
            return forms.PolygonField()

        if geometry_type == Site.MULTIPOINT:
            return forms.MultiPointField()

        if geometry_type == Site.MULTILINESTRING:
            return forms.MultiLineStringField()

        if geometry_type == Site.MULTIPOLYGON:
            return forms.MultiPolygonField()

        raise Http404("Geometry type does not exist")

    def form_invalid(self, form):
        if "locality" in form.data:
            try:
                self.locality = Locality.objects.get(pk=form.data["locality"])

            except Locality.DoesNotExists:
                pass

        return super().form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if hasattr(self, "locality"):
            context["locality"] = self.locality

        return context

    def get_additional_query_on_sucess(self):
        return {
            "site": self.object.pk,
        }
