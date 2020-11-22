from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from irekua_collections.models import Collection
from irekua_collections.models import SamplingEventType
from irekua_permissions.sampling_events import (
    sampling_events as sampling_event_permissions)


class SelectSamplingEventTypeView(TemplateView):
    no_permission_template = 'selia_templates/generic/no_permission.html'
    template_name = 'selia/create/sampling_events/select_type.html'
    navbar_template = 'selia/collection_detail/components/secondary_navbar.html'

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                name=self.request.GET['collection'])

    def has_view_permission(self):
        user = self.request.user
        return sampling_event_permissions.create(user, collection=self.collection)

    def should_redirect(self):
        collection_type = self.collection.collection_type

        if collection_type.restrict_sampling_event_types:
            self.sampling_event_types = collection_type.sampling_event_types.all()
        else:
            self.sampling_event_types = SamplingEventType.objects.all()

        return self.sampling_event_types.count() == 1

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def handle_single_type_redirect(self):
        url = reverse('selia:create_sampling_event')
        full_url = '{url}?{query}&sampling_event_type={pk}'.format(
            url=url,
            query=self.request.GET.urlencode(),
            pk=self.sampling_event_types.first().pk)
        return redirect(full_url)

    def get(self, *args, **kwargs):
        self.get_objects()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        context['sampling_event_types'] = self.sampling_event_types
        return context
