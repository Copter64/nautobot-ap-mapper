"""API views for ap_mapper."""

from nautobot.apps.api import NautobotModelViewSet

from ap_mapper import filters, models
from ap_mapper.api import serializers


class APFloorPlanViewSet(NautobotModelViewSet):
    """APFloorPlan viewset."""

    queryset = models.APFloorPlan.objects.prefetch_related("location", "object_placements")
    serializer_class = serializers.APFloorPlanSerializer
    filterset_class = filters.APFloorPlanFilterSet


class ObjectPlacementViewSet(NautobotModelViewSet):
    """ObjectPlacement viewset."""

    queryset = models.ObjectPlacement.objects.select_related("floor_plan", "content_type")
    serializer_class = serializers.ObjectPlacementSerializer
    filterset_class = filters.ObjectPlacementFilterSet
