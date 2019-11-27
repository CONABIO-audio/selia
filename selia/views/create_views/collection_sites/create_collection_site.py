from django import forms

from irekua_database.models import CollectionSite
from irekua_database.models import Collection
from irekua_database.models import Site
from irekua_database.models import SiteType
from irekua_database.models import SiteDescriptor

from selia.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView
from irekua_permissions.data_collections import sites as site_permissions


class CollectionSiteCreateView(SeliaCreateView):
    model = CollectionSite

    template_name = 'selia/create/collection_sites/create_form.html'
    success_url = 'selia:collection_sites'

    def get_form_class(self):
        site_descriptor_types = self.site_type.site_descriptor_types.all()

        class Form(forms.ModelForm):
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

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.type_fields = set()
                for site_descriptor_type in site_descriptor_types:
                    name = site_descriptor_type.name
                    queryset = SiteDescriptor.objects.filter(descriptor_type=site_descriptor_type)
                    field = forms.ModelChoiceField(queryset, label=name)
                    self.fields[name] = field
                    self.type_fields.add(name)

        return Form

    def save_form(self, form):
        created_object = form.save(commit=False)
        created_object.created_by = self.request.user
        created_object.save()

        descriptors = [form.cleaned_data[name] for name in form.type_fields]
        created_object.site_descriptors.add(*descriptors)
        created_object.save()
        return created_object

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user, collection=self.collection)

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(name=self.request.GET['collection'])

        if not hasattr(self, 'site'):
            self.site = Site.objects.get(pk=self.request.GET['site'])

        if not hasattr(self, 'site_type'):
            self.site_type = SiteType.objects.get(pk=self.request.GET['site_type'])

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
