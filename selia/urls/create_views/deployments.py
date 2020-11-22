from django.urls import path
from selia.views.create_views import deployments


urlpatterns = [
    path(
        "deployments/create/",
        deployments.CreateDeploymentManager.as_view(),
        name="create_deployment",
    ),
    path(
        "deployments/create/1/",
        deployments.SelectDeploymentCollectionView.as_view(),
        name="create_deployment_select_collection",
    ),
    path(
        "deployments/create/2/",
        deployments.SelectDeploymentSamplingEventView.as_view(),
        name="create_deployment_select_sampling_event",
    ),
    path(
        "deployments/create/3/",
        deployments.SelectDeploymentCollectionDeviceView.as_view(),
        name="create_deployment_select_collection_device",
    ),
    path(
        "deployments/create/4/",
        deployments.CreateDeploymentView.as_view(),
        name="create_deployment_create_form",
    ),
]
