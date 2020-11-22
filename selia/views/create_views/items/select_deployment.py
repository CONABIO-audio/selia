from irekua_collections.models import Deployment
from irekua_collections.models import SamplingEvent

from irekua_collections.filters import (
    deployments as deployment_filters,
)
from irekua_permissions.items import items as item_permissions

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectItemDeploymentView(SeliaSelectView):
    template_name = "selia/create/items/select_deployment.html"
    prefix = "deployment"
    create_url = "selia:create_item"

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.create(user, sampling_event=self.sampling_event)

    def get_objects(self):
        if not hasattr(self, "sampling_event"):
            self.sampling_event = SamplingEvent.objects.get(
                pk=self.request.GET["sampling_event"]
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sampling_event"] = self.sampling_event
        context["collection"] = self.sampling_event.collection
        return context

    def get_list_class(self):
        sampling_event = self.request.GET["sampling_event"]

        class DeploymentList(SeliaList):
            filter_class = deployment_filters.Filter
            search_fields = deployment_filters.search_fields
            ordering_fields = deployment_filters.ordering_fields

            queryset = Deployment.objects.filter(sampling_event__pk=sampling_event)

            list_item_template = "selia/select_list_items/deployments.html"
            filter_form_template = "selia/filters/deployment.html"

        return DeploymentList
