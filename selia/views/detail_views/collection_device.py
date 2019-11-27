from django.views.generic.detail import SingleObjectMixin
from django import forms

from irekua_database.models import CollectionDevice
from irekua_database.models import CollectionDeviceType
from irekua_permissions.data_collections import devices as devices_permissions
from irekua_permissions.data_collections import users as user_permissions
from irekua_permissions import licences as licence_permissions
from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionDevice
        fields = [
            'internal_id',
            'metadata',
        ]


class DetailCollectionDeviceView(SeliaDetailView, SingleObjectMixin):
    model = CollectionDevice
    form_class = CollectionDeviceUpdateForm
    delete_redirect_url = 'selia:collection_sampling_events'

    template_name = 'selia/detail/collection_device.html'

    help_template = 'selia/help/collection_device_detail.html'
    detail_template = 'selia/details/collection_device.html'
    summary_template = 'selia/summaries/collection_device.html'
    update_form_template = 'selia/update/collection_device.html'

    def has_view_permission(self):
        user = self.request.user
        return devices_permissions.view(user, collection_device=self.object)

    def has_change_permission(self):
        user = self.request.user
        return devices_permissions.change(user, collection_device=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return devices_permissions.delete(user, collection_device=self.object)

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions['list_collection_users'] = user_permissions.list(
            user, collection=self.object.collection)
        permissions['list_collection_licences'] = licence_permissions.list(
            user, collection=self.object.collection)
        return permissions

    def get_delete_redirect_url_args(self):
        return [self.object.collection.name]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_device'] = self.object
        context['collection'] = self.object.collection

        collection_device_type = CollectionDeviceType.objects.get(
            collection_type=self.object.collection.collection_type,
            device_type=self.object.physical_device.device.device_type)
        context['collection_device_type'] = collection_device_type
        schema = collection_device_type.metadata_schema
        context['form'].fields['metadata'].update_schema(schema)
        return context
