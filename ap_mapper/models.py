"""Database models for AP Mapper."""

from __future__ import annotations

import re

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from nautobot.apps.models import PrimaryModel
from nautobot.core.constants import CHARFIELD_MAX_LENGTH
from nautobot.dcim import models as dcim_models

HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
validate_hex_color = RegexValidator(HEX_COLOR_RE, "Enter a valid hex color (e.g. #RRGGBB).")

MAX_LOGICAL_SIZE = 1_000_000


class APFloorPlan(PrimaryModel):
    """A floor plan map canvas owned by a Nautobot Location.

    Supports a background image (PNG/JPEG/SVG) and stores object placements
    as pixel coordinates relative to the image dimensions.
    """

    location = models.OneToOneField(
        to=dcim_models.Location,
        on_delete=models.CASCADE,
        related_name="ap_mapper_floor_plan",
        help_text="The Location that owns this floor plan map.",
    )
    name = models.CharField(
        max_length=CHARFIELD_MAX_LENGTH,
        blank=True,
        help_text="Optional display name for this floor plan (defaults to Location name).",
    )
    description = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    logical_width = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_LOGICAL_SIZE)],
        help_text="Map canvas width in pixels (or logical units).",
    )
    logical_height = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_LOGICAL_SIZE)],
        help_text="Map canvas height in pixels (or logical units).",
    )
    background = models.FileField(
        upload_to="ap_mapper/backgrounds/",
        blank=True,
        null=True,
        help_text="Optional background floor plan image (PNG/JPEG).",
    )
    revision = models.PositiveBigIntegerField(default=1, editable=False)

    natural_key_field_names = ["location"]

    class Meta:
        ordering = ["location__name"]
        verbose_name = "AP floor plan"
        verbose_name_plural = "AP floor plans"
        constraints = [
            models.CheckConstraint(condition=models.Q(logical_width__gte=1), name="ap_mapper_width_gte_1"),
            models.CheckConstraint(condition=models.Q(logical_height__gte=1), name="ap_mapper_height_gte_1"),
            models.CheckConstraint(
                condition=models.Q(logical_width__lte=MAX_LOGICAL_SIZE), name="ap_mapper_width_lte_max"
            ),
            models.CheckConstraint(
                condition=models.Q(logical_height__lte=MAX_LOGICAL_SIZE), name="ap_mapper_height_lte_max"
            ),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="ap_mapper_revision_gte_1"),
        ]

    def __str__(self):
        """Return string representation of the floor plan."""
        return f"{self.name or self.location} AP Map"

    @property
    def display_name(self):
        """Return the display name, falling back to Location name."""
        return self.name or str(self.location)

    def clean(self):
        """Validate model fields; enforce location immutability."""
        super().clean()
        if self.present_in_database:
            old = type(self).objects.only("location_id").get(pk=self.pk)
            if old.location_id != self.location_id:
                raise ValidationError({"location": "Map owner is immutable after creation."})

    def increment_revision(self):
        """Increment the revision counter (called after mutations)."""
        self.revision += 1
        self.save(update_fields=["revision"])


class ObjectPlacement(PrimaryModel):
    """Placement of any Nautobot object on an APFloorPlan.

    Uses a GenericForeignKey so any object type (WirelessAP, Device, Rack, etc.)
    can be placed on the map at pixel coordinates.
    """

    floor_plan = models.ForeignKey(
        APFloorPlan,
        on_delete=models.CASCADE,
        related_name="object_placements",
        help_text="The floor plan this placement belongs to.",
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="ap_mapper_placements")
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    x = models.PositiveIntegerField(help_text="X coordinate (pixels from left edge).")
    y = models.PositiveIntegerField(help_text="Y coordinate (pixels from top edge).")
    color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_hex_color],
        help_text="Optional hex color override (#RRGGBB) for this marker.",
    )
    label = models.CharField(
        max_length=CHARFIELD_MAX_LENGTH,
        blank=True,
        help_text="Optional display label override (defaults to object name).",
    )

    natural_key_field_names = ["floor_plan", "content_type", "object_id"]

    class Meta:
        ordering = ["object_id"]
        verbose_name = "object placement"
        verbose_name_plural = "object placements"
        constraints = [
            models.UniqueConstraint(
                fields=["floor_plan", "content_type", "object_id"],
                name="ap_mapper_unique_placement",
            ),
            models.CheckConstraint(condition=models.Q(x__gte=0), name="ap_mapper_x_gte_0"),
            models.CheckConstraint(condition=models.Q(y__gte=0), name="ap_mapper_y_gte_0"),
        ]
        indexes = [
            models.Index(fields=["content_type", "object_id"], name="ap_mapper_object_idx"),
        ]

    def __str__(self):
        """Return string representation of the placement."""
        return f"{self.object} on {self.floor_plan} at ({self.x}, {self.y})"

    def clean(self):
        """Validate model fields; enforce immutability and bounds."""
        super().clean()
        if self.present_in_database:
            old = type(self).objects.only("floor_plan_id", "content_type_id", "object_id").get(pk=self.pk)
            if old.floor_plan_id != self.floor_plan_id:
                raise ValidationError({"floor_plan": "Placement map is immutable after creation."})
            if old.content_type_id != self.content_type_id or old.object_id != self.object_id:
                raise ValidationError("Placement target is immutable after creation.")
        if self.floor_plan_id:
            if self.x >= self.floor_plan.logical_width or self.y >= self.floor_plan.logical_height:
                raise ValidationError("Placement coordinates exceed map bounds.")

    @property
    def display_label(self):
        """Return the label, falling back to the object's string representation."""
        return self.label or str(self.object)


# GenericRelation on common object types for easy reverse lookups
try:
    from nautobot.wireless.models import WirelessAP

    WirelessAP.ap_mapper_placements = GenericRelation(
        ObjectPlacement,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="wirelessap",
    )
except ImportError:
    pass
