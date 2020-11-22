from django.views.generic.detail import SingleObjectMixin
from django import forms
from django.db.models import Count, Max

from irekua_collections.models import Collection
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from selia_templates.views.detail_base import SeliaDetailView
from selia_templates.forms.json_field import JsonField


class CollectionUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Collection
        fields = [
            'name',
            'description',
            'metadata',
            'logo'
        ]


class DetailCollectionView(SeliaDetailView, SingleObjectMixin):
    form_class = CollectionUpdateForm

    template_name = 'selia_managers/detail/managed_collection.html'
    help_template = 'selia_managers/help/managed_collection_detail.html'
    detail_template = 'selia_managers/details/managed_collection.html'
    update_form_template = 'selia_managers/update/managed_collection.html'
    summary_template = 'selia_managers/summaries/managed_collection.html'

    delete_redirect_url = 'selia_managers:collections'

    def has_view_permission(self):
        user = self.request.user
        collection_type = self.object.collection_type
        return permissions.view(user, collection_type=collection_type)

    def has_change_permission(self):
        user = self.request.user
        collection_type = self.object.collection_type
        return permissions.view(user, collection_type=collection_type)

    def has_delete_permission(self):
        user = self.request.user
        collection_type = self.object.collection_type
        return permissions.view(user, collection_type=collection_type)

    def get_object(self, *args, **kwargs):
        return (
            Collection.objects
            .annotate(
                user_count=Count('users', distinct=True),
                admin_count=Count('administrators', distinct=True),
                device_count=Count('collectiondevice', distinct=True),
                sampling_event_count=Count('samplingevent', distinct=True),
                site_count=Count('collectionsite', distinct=True),
                deployment_count=Count('samplingevent__samplingeventdevice', distinct=True),
                item_count=Count('samplingevent__samplingeventdevice__item', distinct=True),
                annotation_count=Count('samplingevent__samplingeventdevice__item__annotation', distinct=True),
                last_item=Max('samplingevent__samplingeventdevice__item__created_on'),
                last_annotation=Max('samplingevent__samplingeventdevice__item__annotation__created_on')
            ).get(pk=self.kwargs['pk']))

    def post(self, *args, **kwargs):
        if 'remove_admin' in self.request.GET:
            print('borrar')

        return super().post(*args, **kwargs)

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        schema = self.object.collection_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
