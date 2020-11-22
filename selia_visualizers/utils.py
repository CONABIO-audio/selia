from irekua_visualizers import models


def get_visualizer_module(item_type):
    visualizer = models.VisualizerItemType.objects.get(
        item_type=item_type,
        is_active=True).visualizer
    return models.VisualizerModule.objects.get(
        visualizer=visualizer,
        is_active=True)
