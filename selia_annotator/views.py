import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from irekua_collections.models import Deployment
from irekua_collections.models import DeploymentType
from irekua_collections.models import CollectionTypeAnnotationType
from irekua_collections.models import CollectionItem
#from irekua_rest_api.serializers import object_types

# from selia_annotator.models import AnnotationToolComponent


class CollectionItemAnnotatorView(TemplateView):
    template_name = 'selia_annotator/annotator.html'
    no_permission_template = 'selia_templates/generic/no_permission.html'

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        self.get_objects()

        return super().get(*args, **kwargs)

    def get_urls(self):
        return {
            # 'terms_autocomplete': reverse(
            #     'irekua_autocomplete:term_autocomplete',
            #     args=[mark_safe('event_type_pk')]),
            # 'item': reverse(
            #     'irekua_rest_api:item-detail',
            #     args=[mark_safe('item_pk')]),
            # 'annotations': reverse(
            #     'irekua_rest_api:item-annotations',
            #     args=[mark_safe('item_pk')]),
            # 'visualizers': reverse('selia_visualizers:get_visualizer'),
            # 'annotation_tools': reverse('selia_annotator:get_annotator'),
        }

    def get_objects(self):
        self.item = get_object_or_404(
            CollectionItem,
            pk=self.request.GET.get('pk', None))

        self.deployment = self.item.deployment
        self.sampling_event = self.item.sampling_event
        self.collection = self.item.collection
        self.collection_type = self.collection.collection_type

        self.item_type = self.item.item_type

    def get_items(self):
        queryset = (
            CollectionItem.objects
            .filter(deployment=self.item.deployment)
            .only('id'))
        return [item.id for item in queryset]

    def get_item_types(self):
        if self.collection_type.restrict_item_types:
            queryset = self.collection_type.item_types.all()
        else:
            queryset = ItemType.objects.all()

        queryset = queryset.filter(
            mime_types__in=self.item_type.mime_types.all())
        queryset = queryset.distinct()

        serializer = object_types.items.DetailSerializer(
            queryset,
            many=True,
            context={'request': self.request})
        return json.dumps(serializer.data)

    def get_annotation_types(self):
        if self.collection_type.restrict_annotation_types:
            queryset = self.collection_type.annotation_types.all()
        else:
            queryset = AnnotationType.objects.all()

        serializer = object_types.annotations.DetailSerializer(
            queryset,
            many=True,
            context={'request': self.request})
        return json.dumps(serializer.data)

    # def get_annotators(self):
    #     if self.collection_type.restrict_annotation_types:
    #         types = self.collection_type.annotation_types.all()
    #     else:
    #         types = AnnotationType.objects.all()
    #
    #     queryset = (
    #         AnnotationToolComponent.objects
    #         .filter(
    #             annotation_tool__annotation_type__in=types,
    #             is_active=True)
    #         .select_related(
    #             'annotation_tool',
    #             'annotation_tool__annotation_type'))
    #
    #     return json.dumps({
    #         item.annotation_tool.annotation_type.id: {
    #             'id': item.id,
    #             'name': item.annotation_tool.name,
    #             'version': item.annotation_tool.version,
    #             'module': item.javascript_file.url,
    #         }
    #         for item in queryset
    #     })

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'items': self.get_items(),
            #'item_types': self.get_item_types(),
            #'annotation_types': self.get_annotation_types(),
            # 'annotators': self.get_annotators(),
            'item': self.item,
            'deployment': self.deployment,
            'sampling_event': self.sampling_event,
            'collection': self.collection,
            'urls': self.get_urls(),
        }
