"""Test APFloorPlan and ObjectPlacement models."""

from django.db import IntegrityError
from django.test import tag
from nautobot.apps.testing import ModelTestCases
from nautobot.dcim import models as dcim_models

from ap_mapper import models
from ap_mapper.tests import fixtures


@tag("unit")
class TestAPFloorPlan(ModelTestCases.BaseModelTestCase):
    """Test APFloorPlan."""

    model = models.APFloorPlan

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        fixtures.create_floorplans()

    def test_create_floorplan_minimal(self):
        # pylint: disable=no-member
        site = dcim_models.Site.objects.create(name="Minimal Site")
        location = dcim_models.Location.objects.create(name="Minimal Loc", site=site)
        fp = models.APFloorPlan.objects.create(
            location=location,
            logical_width=1000,
            logical_height=800,
        )
        self.assertEqual(fp.logical_width, 1000)
        self.assertEqual(fp.revision, 1)
        self.assertEqual(str(fp), "Minimal Loc AP Map")

    def test_display_name_fallback(self):
        fp = models.APFloorPlan.objects.first()
        self.assertIsNotNone(fp.display_name)


@tag("unit")
class TestObjectPlacement(ModelTestCases.BaseModelTestCase):
    """Test ObjectPlacement."""

    model = models.ObjectPlacement

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        fixtures.create_placements()

    def test_create_placement(self):
        placement = models.ObjectPlacement.objects.first()
        self.assertGreaterEqual(placement.x, 0)
        self.assertGreaterEqual(placement.y, 0)

    def test_unique_constraint(self):
        placement = models.ObjectPlacement.objects.first()
        with self.assertRaises(IntegrityError):
            models.ObjectPlacement.objects.create(
                floor_plan=placement.floor_plan,
                content_type=placement.content_type,
                object_id=placement.object_id,
                x=50,
                y=50,
            )
