
from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.contrib.auth.models import Permission
from dal import autocomplete

from irekua_database.models import Device
from irekua_database.models import DeviceBrand
from irekua_database.models import DeviceType

from selia.views.create_views.create_base import SeliaCreateView
from selia.forms.type_field import TypeSelectField
from irekua_permissions.devices import (
    physical_devices as device_permissions)


class SelectDeviceForm(forms.Form):
    device = forms.ModelChoiceField(
        required=False,
        queryset=Device.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='irekua_autocomplete:devices_autocomplete',
            attrs={'style': 'width: 100%'}))
    device_type = TypeSelectField(
        required=False,
        queryset=DeviceType.objects.all())
    brand = forms.ModelChoiceField(
        required=False,
        queryset=DeviceBrand.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='irekua_autocomplete:device_brands_autocomplete',
            attrs={'style': 'width: 100%'}))
    model = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        device = cleaned_data.get("device", None)

        if not device:
            device_type = cleaned_data.get("device_type", None)
            if device_type is None:
                msg = 'No device type was assigned'
                self.add_error('device_type', msg)

            brand = cleaned_data.get("brand", None)
            if brand is None:
                msg = 'No device brand was assigned'
                self.add_error('brand', msg)

            model = cleaned_data.get("model", None)
            if model is None:
                msg = 'No device model was assigned'
                self.add_error('model', msg)


class SelectPhysicalDeviceDeviceView(SeliaCreateView):
    form_class = SelectDeviceForm
    template_name = 'selia/create/physical_devices/select_device.html'

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.create(user)

    def get(self, *args, **kwargs):
        permission = Permission.objects.get(name='Can add Device Brand')
        self.request.user.user_permissions.add(permission)
        return super().get(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs.pop('instance')
        return form_kwargs

    def redirect_on_success(self):
        url = reverse('selia:create_physical_device')
        query = self.request.GET.copy()
        query['device'] = self.object.pk

        full_url = '{url}?{query}'.format(url=url, query=query.urlencode())
        return redirect(full_url)

    def save_form(self, form):
        device = form.cleaned_data['device']

        if device is not None:
            return device

        data = form.cleaned_data.copy()
        data.pop('device')
        return Device.objects.create(**data)
