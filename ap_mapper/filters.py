"""Filtering for ap_mapper."""

from nautobot.apps.filters import ContentTypeFilter, MultiValueCharFilter, NameSearchFilterSet, NautobotFilterSet

from ap_mapper import models


class APFloorPlanFilterSet(NameSearchFilterSet, NautobotFilterSet):
    """Filter for APFloorPlan."""

    class Meta:
        model = models.APFloorPlan
        fields = ["location", "name", "description", "logical_width", "logical_height"]


class ObjectPlacementFilterSet(NameSearchFilterSet, NautobotFilterSet):
    """Filter for ObjectPlacement."""

    floor_plan_id = MultiValueCharFilter(field_name="floor_plan__id", lookup_expr="in")
    content_type = ContentTypeFilter()
    object_id = MultiValueCharFilter(field_name="object_id", lookup_expr="in")

    class Meta:
        model = models.ObjectPlacement
        fields = ["floor_plan", "x", "y", "color", "label"]
