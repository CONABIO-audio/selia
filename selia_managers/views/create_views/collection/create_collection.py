from django import forms

from irekua_collections.models import CollectionType
from irekua_collections.models import Collection
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from selia_templates.views.create_base import SeliaCreateView
from selia_templates.forms.json_field import JsonField


class CreateCollectionForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Collection
        fields = [
            'collection_type',
            'name',
            'description',
            'metadata',
            'logo',
            'is_open'
        ]


class CreateCollectionView(SeliaCreateView):
    template_name = 'selia_managers/create/collection/create_form.html'
    success_url = 'selia_managers:collection_detail'

    model = Collection
    form_class = CreateCollectionForm

    def has_view_permission(self):
        return permissions.create(self.request.user)

    def get_initial(self, *args, **kwargs):
        return {
            'collection_type': self.collection_type,
            'is_open': False,
            **super().get_initial(*args, **kwargs)
        }

    def get_success_url_args(self):
        return [self.object.pk]

    def get_context_data(self, *args, **kwargs):
        self.collection_type = CollectionType.objects.get(
            name=self.request.GET['collection_type'])

        return {
            'collection_type': self.collection_type,
            **super().get_context_data(*args, **kwargs)
        }

    def get_form(self, *args, **kwargs):
        if not hasattr(self, 'collection_type'):
            self.collection_type = CollectionType.objects.get(
                name=self.request.GET['collection_type'])

        form = super().get_form(*args, **kwargs)
        schema = self.collection_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form
