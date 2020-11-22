from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from selia_visualizers.utils import get_visualizer_module


@require_http_methods(["GET"])
def get_visualizer(request):
    item_type = request.GET.get('item_type', None)
    visualizer_module = get_visualizer_module(item_type)

    response = {
        "visualizer_version": visualizer_module.pk,
        "file_url": visualizer_module.javascript_file.url
    }
    return JsonResponse(response)
