from django.views.generic.detail import SingleObjectMixin
from django import forms

from irekua_database.models import Licence
from irekua_permissions import licences as licence_permissions
from irekua_permissions.data_collections import (
    users as user_permissions)
from irekua_permissions import (
    licences as licence_permissions)

from selia.views.detail_views.base import SeliaDetailView
from selia_templates.forms.json_field import JsonField


class LicenceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Licence
        fields = [
            'metadata',
            'document',
        ]


class DetailLicenceView(SeliaDetailView, SingleObjectMixin):
    model = Licence
    form_class = LicenceUpdateForm
    delete_redirect_url = 'selia:collection_licences'

    template_name = 'selia/detail/licence.html'
    help_template = 'selia/help/collection_licences.html'
    detail_template = 'selia/details/licence.html'
    summary_template = 'selia/summaries/licence.html'
    update_form_template = 'selia/update/licence.html'
    viewer_template = 'selia/viewers/licence.html'

    def has_view_permission(self):
        user = self.request.user
        return licence_permissions.view(user, licence=self.object)

    def has_change_permission(self):
        user = self.request.user
        return licence_permissions.change(user, licence=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return licence_permissions.delete(user, licence=self.object)

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

        context['licence'] = self.object
        context['collection'] = self.object.collection

        schema = self.object.licence_type.metadata_schema
        context['form'].fields['metadata'].update_schema(schema)
        return context
