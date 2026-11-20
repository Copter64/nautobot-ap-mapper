"""Test APFloorPlan Filter."""

from nautobot.apps.testing import FilterTestCases

from ap_mapper import filters, models
from ap_mapper.tests import fixtures


class APFloorPlanFilterTestCase(FilterTestCases.FilterTestCase):
    """APFloorPlan Filter Test Case."""

    queryset = models.APFloorPlan.objects.all()
    filterset = filters.APFloorPlanFilterSet
    generic_filter_tests = (
        ("id",),
        ("created",),
        ("last_updated",),
        ("name",),
    )

    @classmethod
    def setUpTestData(cls):
        fixtures.create_floorplans()

    def test_q_search_name(self):
        params = {"q": "Test Map One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        params = {"q": "nonexistent"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)


class ObjectPlacementFilterTestCase(FilterTestCases.FilterTestCase):
    """ObjectPlacement Filter Test Case."""

    queryset = models.ObjectPlacement.objects.all()
    filterset = filters.ObjectPlacementFilterSet
    generic_filter_tests = (
        ("id",),
    )

    @classmethod
    def setUpTestData(cls):
        fixtures.create_placements()
