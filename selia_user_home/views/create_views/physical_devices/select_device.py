from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_devices.models import Device
from irekua_devices.models import DeviceType
from irekua_devices.models import DeviceBrand
from selia_templates.views import SeliaCreateView


class SelectDeviceFormBase(forms.Form):
    brand = forms.ModelChoiceField(
        required=False,
        queryset=DeviceBrand.objects.all(),
        widget=get_autocomplete_widget(model=DeviceBrand),
        help_text=_("Search for a model brand or register a new one."),
    )
    model = forms.CharField(required=False, help_text=_("Your device model"))

    def clean(self):
        cleaned_data = super().clean()
        device = cleaned_data.get("device", None)

        if not device:
            brand = cleaned_data.get("brand", None)
            if brand is None:
                msg = _("No device brand was assigned")
                self.add_error("brand", msg)

            model = cleaned_data.get("model", None)
            if model is None:
                msg = _("No device model was assigned")
                self.add_error("model", msg)


class SelectPhysicalDeviceDeviceView(SeliaCreateView):
    template_name = "selia_user_home/create/physical_devices/select_device.html"

    def get_form_class(self):
        class SelectDeviceForm(SelectDeviceFormBase):
            device = forms.ModelChoiceField(
                required=False,
                queryset=Device.objects.filter(device_type=self.device_type),
                widget=get_autocomplete_widget(
                    model=Device, query={"device_type": self.device_type.pk}
                ),
            )

        return SelectDeviceForm

    def get(self, *args, **kwargs):
        permission = Permission.objects.get(
            codename="add_devicebrand", content_type__app_label="irekua_devices"
        )
        self.request.user.user_permissions.add(permission)
        return super().get(*args, **kwargs)

    def get_objects(self):
        if not hasattr(self, "device_type"):
            self.device_type = DeviceType.objects.get(
                pk=self.request.GET["device_type"]
            )

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs.pop("instance")
        return form_kwargs

    def redirect_on_success(self):
        url = reverse("selia_user_home:create_physical_device")
        query = self.request.GET.copy()
        query["device"] = self.object.pk
        full_url = "{url}?{query}".format(url=url, query=query.urlencode())
        return redirect(full_url)

    def save_form(self, form):
        device = form.cleaned_data["device"]
        if device is not None:
            return device

        return Device.objects.create(
            device_type=self.device_type,
            brand=form.cleaned_data["brand"],
            model=form.cleaned_data["model"],
        )

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "device_type": self.device_type,
        }
