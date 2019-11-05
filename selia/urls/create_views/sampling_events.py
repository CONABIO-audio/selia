from django.urls import path
from selia.views.create_views import sampling_events


urlpatterns = [
    path(
        'sampling_events/create/',
        sampling_events.CreateSamplingEventManager.as_view(),
        name='create_sampling_event'),
    path(
        'sampling_events/create/1/',
        sampling_events.SelectSamplingEventCollectionView.as_view(),
        name='create_sampling_event_select_collection'),
    path(
        'sampling_events/create/2/',
        sampling_events.SelectSamplingEventTypeView.as_view(),
        name='create_sampling_event_select_type'),
    path(
        'sampling_events/create/3/',
        sampling_events.SelectSamplingEventSiteView.as_view(),
        name='create_sampling_event_select_site'),
    path(
        'sampling_events/create/4/',
        sampling_events.SamplingEventCreateView.as_view(),
        name='create_sampling_event_create_form'),
]
