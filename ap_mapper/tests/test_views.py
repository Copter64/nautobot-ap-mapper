"""Unit tests for views."""

from django.test import tag
from nautobot.apps.testing import ViewTestCases

from ap_mapper import models
from ap_mapper.tests import fixtures


@tag("unit")
class APFloorPlanViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the APFloorPlan views."""

    model = models.APFloorPlan
    bulk_edit_data = {"name": "Bulk edit"}
    form_data = {}
    update_data = {}

    @classmethod
    def setUpTestData(cls):
        cls.site = fixtures.create_site_and_location()[0]
        cls.location = fixtures.create_site_and_location()[1]
        fixtures.create_floorplans()
        cls.form_data = {
            "location": cls.location.pk,
            "name": "Test Map",
            "logical_width": 1000,
            "logical_height": 800,
        }
        cls.update_data = {
            "location": cls.location.pk,
            "name": "Updated Map",
            "logical_width": 1200,
            "logical_height": 900,
        }
