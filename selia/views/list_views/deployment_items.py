from irekua_collections.models import Deployment
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from irekua_collections.models import DeploymentItem
from irekua_collections.filters import deployment_items
from irekua_permissions.items import items as item_permissions
from selia.views.list_views.base import SeliaListView


class ListDeploymentItemsView(SeliaListView, SingleObjectMixin):
    template_name = "selia/list/deployment_items.html"

    list_item_template = "selia/list_items/item.html"
    help_template = "selia/help/deployment_items.html"
    filter_form_template = "selia/filters/item.html"

    empty_message = _("No items are registered to this deployment")

    filter_class = deployment_items.Filter
    search_fields = deployment_items.search_fields
    ordering_fields = deployment_items.ordering_fields

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.list(user, deployment=self.object)

    def has_create_permission(self):
        user = self.request.user
        return item_permissions.create(user, deployment=self.object)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Deployment.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return DeploymentItem.objects.filter(deployment=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["deployment"] = self.object
        context["sampling_event"] = self.object.sampling_event
        context["collection"] = self.object.sampling_event.collection
        return context
