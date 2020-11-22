from django import forms

from irekua_collections.models import CollectionDevice
from irekua_collections.models import Collection
from irekua_devices.models import PhysicalDevice

from selia_templates.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView


class CollectionDeviceCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionDevice
        fields = [
            'physical_device',
            'collection',
            'collection_name',
            'metadata'
        ]


class CreateCollectionDeviceView(SeliaCreateView):
    model = CollectionDevice
    form_class = CollectionDeviceCreateForm

    template_name = 'selia/create/collection_devices/create_form.html'
    success_url = 'selia:collection_devices'

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_initial(self):
        self.collection = Collection.objects.get(
            name=self.request.GET['collection'])
        self.physical_device = PhysicalDevice.objects.get(
            pk=self.request.GET['physical_device'])

        return {
            'collection': self.collection,
            'physical_device': self.physical_device,
        }

    def get_additional_query_on_sucess(self):
        return {
            'collection': self.object.collection.name,
            'collection_device': self.object.pk
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['physical_device'] = self.physical_device

        context['form'].fields['metadata'].update_schema(
            self.physical_device.device.metadata_schema)

        return context
