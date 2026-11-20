"""Test APFloorPlan and ObjectPlacement models."""

from django.contrib.contenttypes.models import ContentType
from nautobot.apps.testing import ModelTestCases
from nautobot.dcim.models import Device, DeviceRole, Manufacturer, Site

from ap_mapper import models
from ap_mapper.tests import fixtures


class TestAPFloorPlan(ModelTestCases.BaseModelTestCase):
    """Test APFloorPlan."""

    model = models.APFloorPlan

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        fixtures.create_floorplans()

    def test_create_floorplan_minimal(self):
        site = Site.objects.create(name="Minimal Site")
        from nautobot.dcim.models import Location
        location = Location.objects.create(name="Minimal Loc", site=site)
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
        with self.assertRaises(Exception):
            models.ObjectPlacement.objects.create(
                floor_plan=placement.floor_plan,
                content_type=placement.content_type,
                object_id=placement.object_id,
                x=50,
                y=50,
            )
