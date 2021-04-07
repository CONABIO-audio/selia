from django.views.generic.detail import SingleObjectMixin

from irekua_collections.models import CollectionAnnotation
from irekua_items.models import Item
from irekua_collections.filters import collection_annotations

from selia.views.list_views.base import SeliaListView


class ListAnnotationView(SeliaListView, SingleObjectMixin):
    paginate_by = 3

    template_name = "selia/list/annotations.html"
    list_item_template = "selia/list_items/annotation.html"
    help_template = "selia/help/item_annotations.html"
    filter_form_template = "selia/filters/annotation.html"

    filter_class = collection_annotations.Filter
    search_fields = collection_annotations.search_fields
    ordering_fields = collection_annotations.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Item.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return CollectionAnnotation.objects.filter(item=self.object)

    def get_next_object(self):
        next_object = (
            CollectionAnnotation.objects.filter(pk__gt=self.kwargs["pk"])
            .order_by("pk")
            .first()
        )
        return next_object

    def get_prev_object(self):
        prev_object = (
            Item.objects.filter(pk__lt=self.kwargs["pk"])
            .order_by("pk")
            .last()
        )
        return prev_object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["item"] = self.object
        context["next_object"] = self.get_next_object()
        context["prev_object"] = self.get_prev_object()
        return context
