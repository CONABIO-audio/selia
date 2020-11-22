from django.shortcuts import render
from django.views.generic import DetailView

from irekua_collections.models import DeploymentItem
from irekua_permissions.items import items
from selia_visualizers import utils


class ItemVisualizerView(DetailView):
    model = Item
    template_name = 'selia_visualizers/visualizer.html'
    no_permission_template = 'selia_templates/generic/no_permission.html'

    def has_view_permission(self):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        return items.view(self.request.user, item=self.object)

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        try:
            module = utils.get_visualizer_module(self.object.item_type)
        except Exception as error:
            module = None

        return {
            **super().get_context_data(*args, **kwargs),
            'module': module,
        }
