import mimetypes
from django import forms
from django.urls import reverse
from django.utils.http import urlencode

from irekua_database.models import Item
from irekua_database.models import Tag
from irekua_permissions.items import items as item_permissions
from selia_templates.widgets import BootstrapDateTimePickerInput
from selia_visualizers.utils import get_visualizer
from irekua_autocomplete.utils import get_autocomplete_widget

from selia.forms.json_field import JsonField
from selia.views.detail_views.base import SeliaDetailView


mimetypes.init()


class DetailItemView(SeliaDetailView):
    model = Item
    delete_redirect_url = 'selia:collection_items'

    template_name = 'selia/detail/item.html'
    help_template = 'selia/help/collection_item_detail.html'
    detail_template = 'selia/details/item.html'
    summary_template = 'selia/summaries/item.html'
    update_form_template = 'selia/update/item.html'
    viewer_template = 'selia/viewers/item.html'

    def get_form_class(self):
        class Form(forms.ModelForm):
            metadata = JsonField()

            class Meta:
                model = Item
                fields = [
                    'captured_on',
                    'tags',
                    'metadata'
                ]

                widgets = {
                    'tags': get_autocomplete_widget(Tag, multiple=True),
                    'captured_on': BootstrapDateTimePickerInput(),
                }

        return Form

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.view(user, item=self.object)

    def has_change_permission(self):
        return False

    def has_delete_permission(self):
        return False

    def has_download_permission(self):
        user = self.request.user
        return item_permissions.download(user, item=self.object)

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions['download'] = self.has_download_permission()
        return permissions

    def get_visualizer(self):
        item_type = self.object.item_type
        try:
            visualizer = get_visualizer(item_type)
            return visualizer.visualizer_component.javascript_file.url
        except:
            return None

    def get_delete_redirect_url_args(self):
        return [self.object.collection.name]

    def get_next_object(self):
        next_object = (
            Item.objects.filter(
                pk__gt=self.kwargs['pk'],
                sampling_event_device=self.object.sampling_event_device.pk)
            .order_by('pk').first())
        return next_object

    def get_prev_object(self):
        prev_object = (
            Item.objects.filter(
                pk__lt=self.kwargs['pk'],
                sampling_event_device=self.object.sampling_event_device.pk)
            .order_by('pk').last())
        return prev_object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['item'] = self.object
        context['sampling_event_device'] = self.object.sampling_event_device
        context['sampling_event'] = self.object.sampling_event_device.sampling_event
        context['collection'] = self.object.sampling_event_device.sampling_event.collection

        context["next_object"] = self.get_next_object()
        context["prev_object"] = self.get_prev_object()

        context["annotation_app_url"] = '{}?{}'.format(
            reverse('selia_annotator:annotator_app'),
            urlencode({'pk': self.object.pk}))

        if context['permissions']['download']:
            context['visualizer_url'] = self.get_visualizer()
        return context
