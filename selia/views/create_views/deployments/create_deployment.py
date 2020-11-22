from django import forms
from selia.views.create_views.create_base import SeliaCreateView

from irekua_collections.models import Deployment
from irekua_collections.models import SamplingEvent
from irekua_collections.models import CollectionDevice

# from irekua_collections.models import DeploymentTypeDeviceType
from irekua_permissions.sampling_events import devices as device_permissions

from selia_templates.widgets import BootstrapDateTimePickerInput
from selia_templates.forms.json_field import JsonField


class CreateDeploymentForm(forms.ModelForm):
    metadata = JsonField()
    configuration = JsonField()

    class Meta:
        model = Deployment
        fields = [
            "sampling_event",
            "collection_device",
            "metadata",
            "commentaries",
            "configuration",
            "deployed_on",
            "recovered_on",
            "latitude",
            "longitude",
            "altitude",
            "geo_ref",
        ]

        widgets = {
            "deployed_on": BootstrapDateTimePickerInput(),
            "recovered_on": BootstrapDateTimePickerInput(),
        }


class CreateDeploymentView(SeliaCreateView):
    model = Deployment
    form_class = CreateDeploymentForm

    template_name = "selia/create/deployments/create_form.html"
    success_url = "selia:deployments"

    def get_success_url_args(self):
        return [self.request.GET["sampling_event"]]

    def get_additional_query_on_sucess(self):
        sampling_event = self.object.sampling_event
        return {
            "collection": sampling_event.collection.name,
            "sampling_event": sampling_event.pk,
            "deployment": self.object.pk,
        }

    def get_objects(self):
        if not hasattr(self, "sampling_event"):
            self.sampling_event = SamplingEvent.objects.get(
                pk=self.request.GET["sampling_event"]
            )
        if not hasattr(self, "collection_device"):
            self.collection_device = CollectionDevice.objects.get(
                pk=self.request.GET["collection_device"]
            )

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.create(user, sampling_event=self.sampling_event)

    def get_initial(self):
        geometry = self.sampling_event.collection_site.site.geom()
        centroid = geometry.centroid

        return {
            "sampling_event": self.sampling_event,
            "collection_device": self.collection_device,
            "deployed_on": self.sampling_event.started_on,
            "recovered_on": self.sampling_event.ended_on,
            "longitude": centroid.longitude,
            "latitude": centroid.latitude,
            # TODO: Fix initial altitude
            "altitude": None,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["collection"] = self.sampling_event.collection
        context["sampling_event"] = self.sampling_event
        context["collection_device"] = self.collection_device

        # device = self.collection_device.physical_device.device

        # if self.sampling_event.sampling_event_type.restrict_device_types:
        #     info = SamplingEventTypeDeviceType.objects.get(
        #         sampling_event_type=self.sampling_event.sampling_event_type,
        #         device_type=device.device_type,
        #     )
        #
        #     context["info"] = info
        #     context["form"].fields["metadata"].update_schema(info.metadata_schema)
        #
        #     context["form"].fields["configuration"].update_schema(
        #         device.configuration_schema
        #     )
        return context
