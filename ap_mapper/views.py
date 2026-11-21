"""Views for ap_mapper."""

from django.shortcuts import get_object_or_404, render
from nautobot.apps.ui import ObjectDetailContent, ObjectFieldsPanel, SectionChoices
from nautobot.apps.views import GenericView, NautobotUIViewSet
from nautobot.dcim import models as dcim_models

from ap_mapper import filters, forms, models, tables
from ap_mapper.api import serializers


class APFloorPlanUIViewSet(NautobotUIViewSet):
    """ViewSet for APFloorPlan views."""

    bulk_update_form_class = forms.APFloorPlanBulkEditForm
    filterset_class = filters.APFloorPlanFilterSet
    filterset_form_class = forms.APFloorPlanFilterForm
    form_class = forms.APFloorPlanForm
    lookup_field = "pk"
    queryset = models.APFloorPlan.objects.prefetch_related("location", "object_placements")
    serializer_class = serializers.APFloorPlanSerializer
    table_class = tables.APFloorPlanTable

    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields=["location", "name", "description", "logical_width", "logical_height"],
            ),
            ObjectFieldsPanel(
                weight=200,
                section=SectionChoices.RIGHT_HALF,
                fields=["background", "revision"],
            ),
        ],
    )


class ObjectPlacementUIViewSet(NautobotUIViewSet):
    """ViewSet for ObjectPlacement views."""

    bulk_update_form_class = forms.ObjectPlacementBulkEditForm
    filterset_class = filters.ObjectPlacementFilterSet
    filterset_form_class = forms.ObjectPlacementFilterForm
    form_class = forms.ObjectPlacementForm
    lookup_field = "pk"
    queryset = models.ObjectPlacement.objects.select_related("floor_plan", "content_type")
    serializer_class = serializers.ObjectPlacementSerializer
    table_class = tables.ObjectPlacementTable

    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.FULL_WIDTH,
                fields=["floor_plan", "object_type", "x", "y", "color", "label"],
            ),
        ],
    )


class FloorPlanMapView(GenericView):
    """Interactive Leaflet map view for a floor plan.

    Resolves the floor plan either by its own pk or by the associated Location pk.
    Renders the background image with draggable object markers.
    """

    template_name = "ap_mapper/ap_map.html"

    def get(self, request, **kwargs):
        """Render the map view."""
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        """Build context with floor plan and placements data."""
        context = {}

        # Resolve the floor plan
        floor_plan = None

        # Try floor plan pk first
        fp_pk = self.kwargs.get("pk")
        loc_pk = self.kwargs.get("location_pk")

        if fp_pk:
            floor_plan = get_object_or_404(models.APFloorPlan.objects.prefetch_related("object_placements"), pk=fp_pk)
        elif loc_pk:
            try:
                floor_plan = models.APFloorPlan.objects.get(location__pk=loc_pk)
                floor_plan.object_placements.all()  # trigger prefetch
            except models.APFloorPlan.DoesNotExist:
                floor_plan = None

        context["floor_plan"] = floor_plan

        # Location ID for the "Create Floor Plan" link
        context["location_id"] = floor_plan.location_id if floor_plan else ""

        # Build placements data for the JS
        placements = []
        if floor_plan:
            for placement in floor_plan.object_placements.all():
                placements.append(
                    {
                        "id": str(placement.pk),
                        "object_id": placement.object_id,
                        "object_name": placement.display_label,
                        "object_url": placement.object.get_absolute_url()
                        if hasattr(placement.object, "get_absolute_url")
                        else "",
                        "object_type": f"{placement.content_type.app_label}.{placement.content_type.model}",
                        "x": placement.x,
                        "y": placement.y,
                        "color": placement.color or "#0d6efd",
                    }
                )
        context["placements"] = placements

        # Permissions
        context["has_edit_permission"] = self.request.user.has_perm("ap_mapper.change_apfloorplan")
        context["has_placement_add_permission"] = self.request.user.has_perm("ap_mapper.add_objectplacement")
        context["has_placement_change_permission"] = self.request.user.has_perm("ap_mapper.change_objectplacement")

        # API URLs for the JS
        context["api_placements_url"] = "/api/plugins/ap-mapper/placements/"
        context["api_floorplan_url"] = f"/api/plugins/ap-mapper/floor-plans/{floor_plan.pk}/" if floor_plan else ""
        context["csrf_token"] = self.request.META.get("CSRF_COOKIE", "")

        # Picker form
        context["placement_picker_form"] = forms.PlacementPickerForm()

        # Supported object types for the picker
        supported = self.get_supported_types()
        context["supported_types"] = supported
        context["supported_type_options"] = [(t, t.split(".")[-1].replace("_", " ").title()) for t in supported]

        return context

    def get_supported_types(self):
        """Return the list of supported object types for placement."""
        from nautobot.apps.config import get_app_settings_or_config

        supported = get_app_settings_or_config("ap_mapper", "supported_targets")
        if not supported:
            supported = [
                "wireless.wirelessap",
                "dcim.device",
                "dcim.rack",
                "dcim.location",
            ]
        return supported


class DeviceMapView(FloorPlanMapView):
    """Map view scoped to a Device — finds the map containing this device."""

    def get_context_data(self, **kwargs):
        """Build context for device map view."""
        context = super().get_context_data(**kwargs)
        device = get_object_or_404(dcim_models.Device, pk=self.kwargs.get("device_pk"))
        context["device"] = device

        # If no floor plan resolved, try to find one via the device's location
        if not context.get("floor_plan"):
            try:
                floor_plan = models.APFloorPlan.objects.get(location__pk=device.location_id)
                floor_plan.object_placements.all()
                context["floor_plan"] = floor_plan
                # Rebuild placements
                placements = []
                for placement in floor_plan.object_placements.all():
                    placements.append(
                        {
                            "id": str(placement.pk),
                            "object_id": placement.object_id,
                            "object_name": placement.display_label,
                            "object_url": placement.object.get_absolute_url()
                            if hasattr(placement.object, "get_absolute_url")
                            else "",
                            "object_type": f"{placement.content_type.app_label}.{placement.content_type.model}",
                            "x": placement.x,
                            "y": placement.y,
                            "color": placement.color or "#0d6efd",
                        }
                    )
                context["placements"] = placements
            except models.APFloorPlan.DoesNotExist:
                pass

        # Highlight this device if it's placed
        context["focus_object_id"] = str(device.pk)

        return context
