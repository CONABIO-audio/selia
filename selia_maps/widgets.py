from django import forms
from irekua_geo.models import Site


IMAGES = {
    Site.POINT: "selia_maps/point_feature.png",
    Site.LINESTRING: "selia_maps/linestring_feature.png",
    Site.POLYGON: "selia_maps/polygon_feature.png",
    Site.MULTIPOINT: "selia_maps/multipoint_feature.png",
    Site.MULTILINESTRING: "selia_maps/multilinestring_feature.png",
    Site.MULTIPOLYGON: "selia_maps/multipolygon_feature.png",
}


class GeometryTypeSelectWidget(forms.RadioSelect):
    template_name = "selia_templates/widgets/type_input.html"
    option_template_name = "selia_maps/widgets/type_option.html"

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        return {
            **super().create_option(
                name, value, label, selected, index, subindex=subindex, attrs=attrs
            ),
            "image": IMAGES[value],
        }
