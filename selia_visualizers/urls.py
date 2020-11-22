from django.urls import path, include
from selia_visualizers import views
from selia_visualizers.api.router import router


urlpatterns = [
    path('visualize/<pk>/', views.ItemVisualizerView.as_view(), name='item_visualizer'),
    path('api/', include(router.urls)),
    path('', views.get_visualizer, name='get_visualizer'),
]
