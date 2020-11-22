from django import forms
from django.utils.translation import gettext_lazy as _

from irekua_geo.models import Site
from .widgets import GeometryTypeSelectWidget


GEOMETRY_TYPES = (
    (Site.POINT, _("Point")),
    (Site.LINESTRING, _("Line String")),
    (Site.POLYGON, _("Polygon")),
    (Site.MULTIPOINT, _("Multi Point")),
    (Site.MULTILINESTRING, _("Multi Line String")),
    (Site.MULTIPOLYGON, _("Multi Polygon")),
)


class GeometryTypeSelectField(forms.ChoiceField):
    widget = GeometryTypeSelectWidget

    def __init__(self, *args, **kwargs):
        if "choices" not in kwargs:
            kwargs["choices"] = GEOMETRY_TYPES

        super().__init__(*args, **kwargs)
