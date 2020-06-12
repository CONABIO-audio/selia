from django.views.generic.detail import SingleObjectMixin
from django import forms

from irekua_database.models import CollectionSite
from irekua_permissions.data_collections import (
    sites as site_permissions)
from irekua_permissions.data_collections import (
    users as user_permissions)
from irekua_permissions import (
    licences as licence_permissions)
from selia.views.detail_views.base import SeliaDetailView
from selia_templates.forms.json_field import JsonField


class CollectionSiteUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionSite
        fields = [
            'internal_id',
            'metadata',
        ]


class DetailCollectionSiteView(SeliaDetailView, SingleObjectMixin):
    model = CollectionSite
    form_class = CollectionSiteUpdateForm
    delete_redirect_url = 'selia:collection_sites'

    template_name = 'selia/detail/collection_site.html'
    help_template = 'selia/help/collection_site_detail.html'
    detail_template = 'selia/details/collection_site.html'
    summary_template = 'selia/summaries/collection_site.html'
    update_form_template = 'selia/update/collection_site.html'
    viewer_template = 'selia/viewers/collection_site.html'

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.view(user, collection_site=self.object)

    def has_change_permission(self):
        user = self.request.user
        return site_permissions.change(user, collection_site=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return site_permissions.delete(user, collection_site=self.object)

    def get_delete_redirect_url_args(self):
        return [self.object.collection.name]

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions['list_collection_users'] = user_permissions.list(
            user, collection=self.object.collection)
        permissions['list_collection_licences'] = licence_permissions.list(
            user, collection=self.object.collection)
        return permissions

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_site'] = self.object
        context['collection'] = self.object.collection

        schema = self.object.site_type.metadata_schema
        context['form'].fields['metadata'].update_schema(schema)
        return context
