from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from irekua_collections.models import SamplingEvent
from irekua_collections.models import Deployment
from irekua_collections.filters import deployments
from irekua_permissions.sampling_events import devices as device_permissions
from selia.views.list_views.base import SeliaListView


class ListDeploymentsView(SeliaListView, SingleObjectMixin):
    template_name = "selia/list/deployments.html"

    list_item_template = "selia/list_items/deployment.html"
    help_template = "selia/help/deployment.html"
    filter_form_template = "selia/filters/deployment.html"

    empty_message = _("No devices are registered in this sampling event")

    filter_class = deployments.Filter
    search_fields = deployments.search_fields
    ordering_fields = deployments.ordering_fields

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.list(user, sampling_event=self.object)

    def has_create_permission(self):
        user = self.request.user
        return device_permissions.create(user, sampling_event=self.object)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SamplingEvent.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Deployment.objects.filter(sampling_event=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sampling_event"] = self.object
        context["collection"] = self.object.collection
        return context
