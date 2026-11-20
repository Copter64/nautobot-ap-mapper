"""API serializers for ap_mapper."""

from rest_framework import serializers

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from ap_mapper import models


class APFloorPlanSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    """APFloorPlan Serializer."""

    location = serializers.SerializerMethodField()
    placement_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.APFloorPlan
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
        return {"id": obj.location.id, "url": obj.location.get_absolute_url(), "name": str(obj.location)}

    def to_representation(self, instance):
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
        return {"id": obj.floor_plan.id, "url": obj.floor_plan.get_absolute_url(), "name": str(obj.floor_plan)}

    def get_object_type(self, obj):
        if obj.content_type:
            return f"{obj.content_type.app_label}.{obj.content_type.model}"
        return None

    def get_object(self, obj):
        if obj.object:
            return {
                "id": obj.object.id,
                "url": obj.object.get_absolute_url() if hasattr(obj.object, "get_absolute_url") else None,
                "name": str(obj.object),
            }
        return None
