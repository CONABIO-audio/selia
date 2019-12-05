from django import forms

from irekua_database.models import SamplingEvent
from irekua_database.models import SamplingEventType
from irekua_database.models import Collection
from irekua_database.models import CollectionSite

from selia_templates.widgets import BootstrapDateTimePickerInput
from selia.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView
from irekua_permissions.sampling_events import (
    sampling_events as sampling_event_permissions)


class SamplingEventCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'sampling_event_type',
            'collection_site',
            'metadata',
            'started_on',
            'ended_on',
            'collection'
        ]

        widgets = {
            'started_on': BootstrapDateTimePickerInput(),
            'ended_on': BootstrapDateTimePickerInput(),
        }


class SamplingEventCreateView(SeliaCreateView):
    model = SamplingEvent
    form_class = SamplingEventCreateForm

    success_url = 'selia:collection_sampling_events'
    template_name = 'selia/create/sampling_events/create_form.html'

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                name=self.request.GET['collection'])
        if not hasattr(self, 'collection_site'):
            self.collection_site = CollectionSite.objects.get(
                pk=self.request.GET['collection_site'])
        if not hasattr(self, 'sampling_event_type'):
            self.sampling_event_type = SamplingEventType.objects.get(
                pk=self.request.GET['sampling_event_type'])

    def has_view_permission(self):
        user = self.request.user
        return sampling_event_permissions.create(user, collection=self.collection)

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_additional_query_on_sucess(self):
        return {
            'collection': self.object.collection.pk,
            'sampling_event': self.object.pk
        }

    def get_initial(self):
        return {
            'collection': self.collection,
            'collection_site': self.collection_site,
            'sampling_event_type': self.sampling_event_type,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['collection_site'] = self.collection_site
        context['sampling_event_type'] = self.sampling_event_type

        context['form'].fields['metadata'].update_schema(
            self.sampling_event_type.metadata_schema)
        return context
