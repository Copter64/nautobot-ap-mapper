"""Tables for ap_mapper."""

import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ButtonsColumn, ToggleColumn

from ap_mapper import models


class APFloorPlanTable(BaseTable):
    """Table for APFloorPlan list view."""

    pk = ToggleColumn()
    location = tables.Column(linkify=True)
    name = tables.Column(linkify=True, verbose_name="Map Name")
    has_background = tables.BooleanColumn(
        accessor="background",
        verbose_name="Has BG",
        empty_values=(),
    )
    placement_count = tables.Column(verbose_name="Objects")
    actions = ButtonsColumn(
        models.APFloorPlan,
        pk_field="pk",
    )

    class Meta(BaseTable.Meta):
        model = models.APFloorPlan
        fields = (
            "pk",
            "location",
            "name",
            "logical_width",
            "logical_height",
            "has_background",
            "placement_count",
            "actions",
        )
        default_columns = ("pk", "location", "name", "has_background", "placement_count", "actions")


class ObjectPlacementTable(BaseTable):
    """Table for ObjectPlacement list view."""

    pk = ToggleColumn()
    floor_plan = tables.Column(linkify=True)
    object = tables.Column(linkify=True, verbose_name="Object")
    object_type = tables.Column(verbose_name="Type")
    x = tables.Column()
    y = tables.Column()
    color = tables.Column(verbose_name="Color")
    label = tables.Column(verbose_name="Label")
    actions = ButtonsColumn(
        models.ObjectPlacement,
        pk_field="pk",
    )

    class Meta(BaseTable.Meta):
        model = models.ObjectPlacement
        fields = ("pk", "floor_plan", "object", "object_type", "x", "y", "color", "label", "actions")
        default_columns = ("pk", "floor_plan", "object", "object_type", "x", "y", "actions")
