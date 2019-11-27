from django.views.generic.detail import SingleObjectMixin
from django import forms

from irekua_database.models import CollectionUser
from irekua_database.models import SamplingEvent
from irekua_database.models import CollectionSite
from irekua_database.models import CollectionDevice
from irekua_database.models import Item
from irekua_database.models import Annotation
from irekua_permissions.data_collections import users as user_permissions
from irekua_permissions import licences as licence_permissions

from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionUserUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionUser
        fields = [
            'role',
            'metadata',
        ]


class DetailCollectionUserView(SeliaDetailView, SingleObjectMixin):
    model = CollectionUser
    form_class = CollectionUserUpdateForm
    delete_redirect_url = 'selia:collection_users'

    template_name = 'selia/detail/collection_user.html'

    help_template = 'selia/help/collection_user_detail.html'
    detail_template = 'selia/details/collection_user.html'
    summary_template = 'selia/summaries/collection_user.html'
    update_form_template = 'selia/update/collection_user.html'
    viewer_template = 'selia/viewers/collection_user.html'

    def has_view_permission(self):
        user = self.request.user
        return user_permissions.view(user, collection_user=self.object)

    def has_change_permission(self):
        user = self.request.user
        return user_permissions.change(user, collection_user=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return user_permissions.delete(user, collection_user=self.object)

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

    def get_summary_info(self):
        user = self.object.user
        collection = self.object.collection

        sampling_events = (
            SamplingEvent.objects
            .filter(collection=collection, created_by=user)
            .count())
        collection_sites = (
            CollectionSite.objects
            .filter(collection=collection, created_by=user)
            .count())
        collection_devices = (
            CollectionDevice.objects
            .filter(collection=collection, created_by=user)
            .count())
        items = (
            Item.objects
            .filter(
                sampling_event_device__sampling_event__collection=collection,
                created_by=user)
            .count())
        annotations = (
            Annotation.objects
            .filter(
                item__sampling_event_device__sampling_event__collection=collection,
                created_by=user)
            .count())

        return {
            'sampling_events': sampling_events,
            'collection_sites': collection_sites,
            'collection_devices': collection_devices,
            'items': items,
            'annotations': annotations,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object.collection
        context['summary_info'] = self.get_summary_info()
        return context
