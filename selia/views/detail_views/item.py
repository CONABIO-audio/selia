import mimetypes
from django import forms

from irekua_database.models import Item
from irekua_permissions.items import items as item_permissions

from selia_visualizers.utils import get_visualizer

from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


mimetypes.init()


class CollectionItemUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Item
        fields = [
            'sampling_event_device',
            'captured_on',
            'tags',
            'metadata'
        ]


class DetailItemView(SeliaDetailView):
    model = Item
    form_class = CollectionItemUpdateForm
    delete_redirect_url = 'selia:collection_items'

    template_name = 'selia/detail/item.html'
    help_template = 'selia/help/collection_item_detail.html'
    detail_template = 'selia/details/item.html'
    summary_template = 'selia/summaries/item.html'
    update_form_template = 'selia/update/item.html'
    viewer_template = 'selia/viewers/item.html'

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.view(user, item=self.object)

    def has_change_permission(self):
        user = self.request.user
        return item_permissions.change(user, item=self.object)

    def has_delete_permission(self):
        user = self.request.user
        return item_permissions.delete(user, item=self.object)

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
        next_object = Item.objects.filter(pk__gt=self.kwargs['pk']).order_by('pk').first()
        return next_object

    def get_prev_object(self):
        prev_object = Item.objects.filter(pk__lt=self.kwargs['pk']).order_by('pk').last()
        return prev_object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection_device'] = self.object
        context["next_object"] = self.get_next_object()
        context["prev_object"] = self.get_prev_object()

        if context['permissions']['download']:
            context['visualizer_url'] = self.get_visualizer()
        return context
