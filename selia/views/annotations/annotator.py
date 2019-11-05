from django.urls import reverse
from django.utils.html import mark_safe

from irekua_database.models import Item
from selia.views.annotations.base import SeliaAnnotationView


class CollectionItemAnnotatorView(SeliaAnnotationView):
    template_name = 'selia/annotations/annotator.html'

    def get_urls(self):
        collection = self.item.sampling_event_device.sampling_event.collection
        return {
            'terms_autocomplete': reverse(
                'irekua_autocomplete:term_autocomplete',
                args=[mark_safe('event_type_pk')]),
            'item': reverse(
                'rest-api:item-detail',
                args=[self.item.pk]),
            'item_type': reverse(
                'rest-api:itemtype-detail',
                args=[self.item.item_type.pk]),
            'annotation_types': reverse(
                'rest-api:collectiontype-annotation-types',
                args=[collection.collection_type.pk]),
            'annotations': reverse(
                'rest-api:item-annotations',
                args=[self.item.pk]),
            'annotation_detail': reverse(
                'rest-api:annotation-detail',
                args=[mark_safe('annotation_pk')]),
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.item = Item.objects.get(pk=self.kwargs['pk'])
        context['item'] = self.item
        context['urls'] = self.get_urls()
        return context
