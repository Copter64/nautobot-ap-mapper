"""Test AP Mapper forms."""

from django.test import TestCase
from nautobot.dcim.models import Location, Site

from ap_mapper import forms


class APFloorPlanFormTest(TestCase):
    """Test APFloorPlan forms."""

    @classmethod
    def setUpTestData(cls):
        cls.site = Site.objects.create(name="Form Test Site")
        cls.location = Location.objects.create(name="Form Test Loc", site=cls.site)

    def test_specifying_all_fields_success(self):
        form = forms.APFloorPlanForm(
            data={
                "location": self.location.pk,
                "name": "Development",
                "description": "Development Testing",
                "logical_width": 1000,
                "logical_height": 800,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_validate_location_required(self):
        form = forms.APFloorPlanForm(
            data={
                "name": "Development",
                "logical_width": 1000,
                "logical_height": 800,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("location", form.errors)
