from rest_framework.routers import DefaultRouter
from selia_annotator.api import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'annotations', views.AnnotationViewSet)
router.register(r'collection_types', views.CollectionTypeViewSet)
