from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse

from irekua_devices.models import DeviceType
from selia_templates.views import SeliaCreateView
from selia_templates.forms.type_field import TypeSelectField


class SelectDeviceType(forms.Form):
    device_type = TypeSelectField(required=False, queryset=DeviceType.objects.all())


class SelectPhysicalDeviceDeviceTypeView(SeliaCreateView):
    form_class = SelectDeviceType
    template_name = "selia_user_home/create/physical_devices/select_device_type.html"

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs.pop("instance")
        return form_kwargs

    def redirect_on_success(self):
        url = reverse("selia_user_home:create_physical_device")
        query = self.request.GET.copy()
        query["device_type"] = self.object.pk
        full_url = "{url}?{query}".format(url=url, query=query.urlencode())
        return redirect(full_url)

    def save_form(self, form):
        device_type = form.cleaned_data["device_type"]
        if device_type is not None:
            return device_type
        return DeviceType.objects.get(pk=device_type)
