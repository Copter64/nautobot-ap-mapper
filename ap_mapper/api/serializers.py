"""API serializers for ap_mapper."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin
from rest_framework import serializers

from ap_mapper import models


class APFloorPlanSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    """APFloorPlan Serializer."""

    location = serializers.SerializerMethodField()
    placement_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.APFloorPlan
        # Keep explicit fields to include SerializerMethodField entries.
        # pylint: disable-next=nb-use-fields-all
        fields = [
            "id",
            "url",
            "location",
            "name",
            "description",
            "logical_width",
            "logical_height",
            "background",
            "revision",
            "placement_count",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        read_only_fields = ["revision"]

    def get_location(self, obj):
        """Return location reference data."""
        return {"id": obj.location.id, "url": obj.location.get_absolute_url(), "name": str(obj.location)}

    def to_representation(self, instance):
        """Add placement count to representation."""
        ret = super().to_representation(instance)
        ret["placement_count"] = instance.object_placements.count()
        return ret


class ObjectPlacementSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    """ObjectPlacement Serializer."""

    floor_plan = serializers.SerializerMethodField()
    object_type = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()

    class Meta:
        model = models.ObjectPlacement
        # Keep explicit fields to include SerializerMethodField entries.
        # pylint: disable-next=nb-use-fields-all
        fields = [
            "id",
            "url",
            "floor_plan",
            "content_type",
            "object_id",
            "object",
            "object_type",
            "x",
            "y",
            "color",
            "label",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]

    def get_floor_plan(self, obj):
        """Return floor plan reference data."""
        return {"id": obj.floor_plan.id, "url": obj.floor_plan.get_absolute_url(), "name": str(obj.floor_plan)}

    def get_object_type(self, obj):
        """Return the content type label for the placed object."""
        if obj.content_type:
            return f"{obj.content_type.app_label}.{obj.content_type.model}"
        return None

    def get_object(self, obj):
        """Return the placed object reference data."""
        if obj.object:
            return {
                "id": obj.object.id,
                "url": obj.object.get_absolute_url() if hasattr(obj.object, "get_absolute_url") else None,
                "name": str(obj.object),
            }
        return None
