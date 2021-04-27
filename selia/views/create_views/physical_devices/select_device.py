
from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.contrib.auth.models import Permission
from irekua_database.autocomplete import get_autocomplete_widget

from irekua_devices.models import Device
from irekua_devices.models import DeviceBrand
from irekua_devices.models import DeviceType
from irekua_schemas.models import Schema
from irekua_collections.models import Collection
from irekua_devices.filters import devices as devices_filters

from selia.views.create_views.create_base import SeliaCreateView
from selia_templates.forms.type_field import TypeSelectField
from irekua_permissions.devices import physical_devices as device_permissions
from selia.views.utils import SeliaList




class SelectPhysicalDeviceDeviceView(SeliaCreateView):
    template_name = 'selia/create/physical_devices/select_device.html'
    prefix = "device"
    create_url = "selia:create_physical_device"
    model = Device

    def get_form_class(self):
        class SelectDeviceForm(forms.ModelForm):
            class Meta:
                model = Device
                fields = [
                    "device_type",
                    "brand",
                    "model",
                    "configuration_schema" 
                ]

                widgets = {
                    "device_type": get_autocomplete_widget(model=DeviceType),
                    "brand": get_autocomplete_widget(model=DeviceBrand),
                    "configuration_schema": get_autocomplete_widget(model=Schema)
                }

        return SelectDeviceForm


    def has_view_permission(self):
        user = self.request.user
        return device_permissions.create(user)

    def get_objects(self):
        if not hasattr(self, "collection"):
            self.collection = Collection.objects.get(
                name=self.request.GET["collection"]
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        context["collection"] = self.collection
        context["list"] = self.get_device_list()
        context["prefix"] = self.prefix
        context["create_url"] = self.create_url

        return context

    def redirect_on_success(self):
        url = reverse('selia:create_physical_device')
        query = self.request.GET.copy()
        query['device'] = self.object.pk

        full_url = '{url}?{query}'.format(url=url, query=query.urlencode())
        return redirect(full_url)


    def get_device_list(self):
        devices = Device.objects.all()

        class DeviceList(SeliaList):
            prefix = "devices"

            filter_class = devices_filters.Filter
            search_fields = devices_filters.search_fields
            ordering_fields = devices_filters.ordering_fields

            queryset = devices

            list_item_template = "selia/select_list_items/devices.html"
            filter_form_template = "selia/filters/device.html"

        device_list = DeviceList(self.request)
        return device_list.get_context_data()
