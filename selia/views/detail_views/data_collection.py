from django import forms
from dal import autocomplete

from irekua_database.models import Collection
from irekua_permissions.data_collections import data_collections as collection_permissions
from irekua_permissions.data_collections import users as user_permissions
from irekua_permissions import licences as licence_permissions
from selia.views.detail_views.base import SeliaDetailView
from selia_templates.forms.json_field import JsonField


class CollectionUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Collection
        fields = [
            'name',
            'institution',
            'description',
            'metadata',
            'logo'
        ]

        widgets = {
            'institution': autocomplete.ModelSelect2(
                url='irekua_autocomplete:institutions_autocomplete'
            )
        }


class DetailCollectionView(SeliaDetailView):
    model = Collection
    form_class = CollectionUpdateForm

    template_name = 'selia/detail/collection.html'
    slug_url_kwarg = 'name'
    slug_field = 'name'

    help_template = 'selia/help/collection_detail.html'
    detail_template = 'selia/details/collection.html'
    summary_template = 'selia/summaries/collection.html'
    update_form_template = 'selia/update/collection.html'

    def has_view_permission(self):
        user = self.request.user
        return collection_permissions.view(user, collection=self.object)

    def has_change_permission(self):
        user = self.request.user
        return collection_permissions.change(user, collection=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return collection_permissions.delete(user, collection=self.object)

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions['list_collection_users'] = user_permissions.list(
            user, collection=self.object)
        permissions['list_collection_licences'] = licence_permissions.list(
            user, collection=self.object)
        return permissions

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        schema = self.object.collection_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
