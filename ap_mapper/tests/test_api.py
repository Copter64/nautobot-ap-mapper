"""Unit tests for ap_mapper API."""

from nautobot.apps.testing import APIViewTestCases

from ap_mapper import models
from ap_mapper.tests import fixtures


class APFloorPlanAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the API viewsets for APFloorPlan."""

    model = models.APFloorPlan
    choices_fields = ()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        fixtures.create_floorplans()
        cls.create_data = [
            {
                "location": fixtures.create_site_and_location()[1].pk,
                "name": "API Test One",
                "logical_width": 1000,
                "logical_height": 800,
            },
            {
                "location": fixtures.create_site_and_location()[1].pk,
                "name": "API Test Two",
                "logical_width": 1200,
                "logical_height": 900,
            },
            {
                "location": fixtures.create_site_and_location()[1].pk,
                "name": "API Test Three",
                "logical_width": 800,
                "logical_height": 600,
            },
        ]
        cls.update_data = {
            "name": "Update Test Two",
            "logical_width": 1500,
        }
        cls.bulk_update_data = {
            "name": "Bulk Updated",
        }
