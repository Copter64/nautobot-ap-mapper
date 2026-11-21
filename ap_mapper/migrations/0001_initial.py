"""Initial migration for AP Mapper models."""

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("dcim", "0084_add_module_type_image_support"),
    ]

    operations = [
        migrations.CreateModel(
            name="APFloorPlan",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="created",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        verbose_name="last updated",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=200,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Optional display name for this floor plan (defaults to Location name).",
                        max_length=255,
                    ),
                ),
                (
                    "logical_width",
                    models.PositiveIntegerField(
                        help_text="Map canvas width in pixels (or logical units).",
                    ),
                ),
                (
                    "logical_height",
                    models.PositiveIntegerField(
                        help_text="Map canvas height in pixels (or logical units).",
                    ),
                ),
                (
                    "background",
                    models.FileField(
                        blank=True,
                        help_text="Optional background floor plan image (PNG/JPEG).",
                        null=True,
                        upload_to="ap_mapper/backgrounds/",
                    ),
                ),
                (
                    "revision",
                    models.PositiveBigIntegerField(
                        default=1,
                        editable=False,
                    ),
                ),
                (
                    "location",
                    models.OneToOneField(
                        help_text="The Location that owns this floor plan map.",
                        on_delete=models.CASCADE,
                        related_name="ap_mapper_floor_plan",
                        to="dcim.location",
                    ),
                ),
                (
                    "_custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        editable=False,
                    ),
                ),
            ],
            options={
                "verbose_name": "AP floor plan",
                "verbose_name_plural": "AP floor plans",
                "ordering": ["location__name"],
            },
        ),
        migrations.CreateModel(
            name="ObjectPlacement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="created",
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        verbose_name="last updated",
                    ),
                ),
                (
                    "object_id",
                    models.UUIDField(db_index=True),
                ),
                (
                    "x",
                    models.PositiveIntegerField(
                        help_text="X coordinate (pixels from left edge).",
                    ),
                ),
                (
                    "y",
                    models.PositiveIntegerField(
                        help_text="Y coordinate (pixels from top edge).",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        blank=True,
                        help_text="Optional hex color override (#RRGGBB) for this marker.",
                        max_length=7,
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text="Optional display label override (defaults to object name).",
                        max_length=255,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="ap_mapper_placements",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "floor_plan",
                    models.ForeignKey(
                        help_text="The floor plan this placement belongs to.",
                        on_delete=models.CASCADE,
                        related_name="object_placements",
                        to="ap_mapper.apfloorplan",
                    ),
                ),
                (
                    "_custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        editable=False,
                    ),
                ),
            ],
            options={
                "verbose_name": "object placement",
                "verbose_name_plural": "object placements",
                "ordering": ["object_id"],
            },
        ),
        migrations.AddConstraint(
            model_name="apfloorplan",
            constraint=models.CheckConstraint(
                condition=models.Q(("logical_width__gte", 1)),
                name="ap_mapper_width_gte_1",
            ),
        ),
        migrations.AddConstraint(
            model_name="apfloorplan",
            constraint=models.CheckConstraint(
                condition=models.Q(("logical_height__gte", 1)),
                name="ap_mapper_height_gte_1",
            ),
        ),
        migrations.AddConstraint(
            model_name="apfloorplan",
            constraint=models.CheckConstraint(
                condition=models.Q(("logical_width__lte", 1000000)),
                name="ap_mapper_width_lte_max",
            ),
        ),
        migrations.AddConstraint(
            model_name="apfloorplan",
            constraint=models.CheckConstraint(
                condition=models.Q(("logical_height__lte", 1000000)),
                name="ap_mapper_height_lte_max",
            ),
        ),
        migrations.AddConstraint(
            model_name="apfloorplan",
            constraint=models.CheckConstraint(
                condition=models.Q(("revision__gte", 1)),
                name="ap_mapper_revision_gte_1",
            ),
        ),
        migrations.AddConstraint(
            model_name="objectplacement",
            constraint=models.UniqueConstraint(
                fields=("floor_plan", "content_type", "object_id"),
                name="ap_mapper_unique_placement",
            ),
        ),
        migrations.AddConstraint(
            model_name="objectplacement",
            constraint=models.CheckConstraint(
                condition=models.Q(("x__gte", 0)),
                name="ap_mapper_x_gte_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="objectplacement",
            constraint=models.CheckConstraint(
                condition=models.Q(("y__gte", 0)),
                name="ap_mapper_y_gte_0",
            ),
        ),
        migrations.AddIndex(
            model_name="objectplacement",
            index=models.Index(
                fields=["content_type", "object_id"],
                name="ap_mapper_object_idx",
            ),
        ),
    ]
