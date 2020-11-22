from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse

from selia_maps.fields import GeometryTypeSelectField
from selia_templates.views import SeliaCreateView


class SelectGeometryType(forms.Form):
    geometry_type = GeometryTypeSelectField()


class SelectGeometryTypeView(SeliaCreateView):
    form_class = SelectGeometryType
    template_name = "selia_user_home/create/sites/select_geometry_type.html"

    def redirect_on_success(self):
        url = reverse("selia_user_home:create_site")
        query = self.request.GET.copy()
        query["geometry_type"] = self.object
        full_url = "{url}?{query}".format(url=url, query=query.urlencode())
        return redirect(full_url)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs.pop("instance")
        return form_kwargs

    def save_form(self, form):
        return form.cleaned_data["geometry_type"]
