from django import forms

from irekua_database.models import CollectionSite
from irekua_database.models import Collection
from irekua_database.models import Site
from irekua_database.models import SiteType

from selia.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView
from irekua_permissions.data_collections import (
    sites as site_permissions)


class CollectionSiteCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionSite
        fields = [
            'site_type',
            'metadata',
            'site',
            'collection',
            'internal_id',
        ]


class CollectionSiteCreateView(SeliaCreateView):
    model = CollectionSite
    form_class = CollectionSiteCreateForm

    template_name = 'selia/create/collection_sites/create_form.html'
    success_url = 'selia:collection_sites'

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user, collection=self.collection)

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                name=self.request.GET['collection'])

        if not hasattr(self, 'site'):
            self.site = Site.objects.get(
                pk=self.request.GET['site'])

        if not hasattr(self, 'site_type'):
            self.site_type = SiteType.objects.get(
                pk=self.request.GET['site_type'])

    def get_initial(self):
        return {
            'collection': self.collection,
            'site': self.site,
            'site_type': self.site_type,
        }

    def get_additional_query_on_sucess(self):
        return {
            'collection': self.object.collection.pk,
            'collection_site': self.object.pk
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['site'] = self.site
        context['site_type'] = self.site_type

        context['form'].fields['metadata'].update_schema(
            self.site_type.metadata_schema)

        return context
