from rest_framework.routers import DefaultRouter
from selia_visualizers.api import views

router = DefaultRouter()
router.register(r'visualizers', views.VisualizerViewSet)
router.register(r'visualizer_versions', views.VisualizerVersionViewSet)
