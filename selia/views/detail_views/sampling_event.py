import json
from django import forms

from irekua_collections.models import SamplingEvent
import irekua_permissions.sampling_events.sampling_events as sampling_event_permissions
from selia_templates.forms.json_field import JsonField
from selia_templates.widgets import BootstrapDateTimePickerInput
from selia.views.detail_views.base import SeliaDetailView


class SamplingEventUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'started_on',
            'ended_on',
            'commentaries',
            'metadata',
        ]

        widgets = {
            'started_on': BootstrapDateTimePickerInput(),
            'ended_on': BootstrapDateTimePickerInput(),
        }


class DetailSamplingEventView(SeliaDetailView):
    model = SamplingEvent
    form_class = SamplingEventUpdateForm
    delete_redirect_url = 'selia:collection_sampling_events'

    template_name = 'selia/detail/sampling_event.html'

    help_template = 'selia/help/collection_sampling_events.html'
    summary_template = 'selia/summaries/sampling_event.html'
    detail_template = 'selia/details/sampling_event.html'
    update_form_template = 'selia/update/sampling_event.html'
    viewer_template = 'selia/viewers/sampling_event.html'

    def has_view_permission(self):
        user = self.request.user
        return sampling_event_permissions.view(user, sampling_event=self.object)

    def has_change_permission(self):
        user = self.request.user
        return sampling_event_permissions.change(user, sampling_event=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return sampling_event_permissions.delete(user, sampling_event=self.object)

    def get_delete_redirect_url_args(self):
        return [self.object.collection.name]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        try: 
            self.schema = self.object.sampling_event_type.metadata_schema.schema
        except: 
            self.schema = self.object.sampling_event_type.metadata_schema
        form.fields['metadata'].update_schema(self.schema)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object.collection
        context['sampling_event'] = self.object
        context['schema'] = json.dumps(self.schema)
        return context
