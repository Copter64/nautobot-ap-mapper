"""Test AP Mapper forms."""

from django.test import tag
from nautobot.apps.testing import FormTestCases
from nautobot.dcim import models as dcim_models

from ap_mapper import forms


@tag("unit")
class APFloorPlanFormTest(FormTestCases.BaseFormTestCase):
    """Test APFloorPlan forms."""

    form = forms.APFloorPlanForm

    @classmethod
    def setUpTestData(cls):
        # pylint: disable=no-member
        cls.site = dcim_models.Site.objects.create(name="Form Test Site")
        cls.location = dcim_models.Location.objects.create(name="Form Test Loc", site=cls.site)

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
