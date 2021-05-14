from django.urls import path
from selia_visualizers import views


urlpatterns = [
    path("visualize/<pk>/", views.ItemVisualizerView.as_view(), name="item_visualizer"),
    path("", views.get_visualizer, name="get_visualizer"),
]
