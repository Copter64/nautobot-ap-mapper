"""Create fixtures for tests."""

from django.contrib.contenttypes.models import ContentType
from nautobot.dcim import models as dcim_models

from ap_mapper.models import APFloorPlan, ObjectPlacement


def create_site_and_location():
    """Create a site and location for floor plan tests."""
    site = dcim_models.Site.objects.create(name="Test Site")
    location = dcim_models.Location.objects.create(name="Test Location", site=site)
    return site, location


def create_floorplans():
    """Create APFloorPlan objects for tests."""
    site, location = create_site_and_location()
    site2, location2 = create_site_and_location()
    dcim_models.Site.objects.filter(name="Test Site").update(name="Test Site 2")
    dcim_models.Location.objects.filter(name="Test Location", site=site2).update(name="Test Location 2")

    floorplan1 = APFloorPlan.objects.create(
        location=location,
        name="Test Map One",
        logical_width=1000,
        logical_height=800,
    )
    floorplan2 = APFloorPlan.objects.create(
        location=location2,
        name="Test Map Two",
        logical_width=1200,
        logical_height=900,
    )
    return floorplan1, floorplan2


def create_placements():
    """Create ObjectPlacement objects for tests."""
    floorplan1, floorplan2 = create_floorplans()

    # Create a device to place
    role = dcim_models.DeviceRole.objects.get_or_create(name="Test Role")[0]
    device = dcim_models.Device.objects.create(
        name="test-ap-01",
        device_type=None,
        site=floorplan1.location.site,
        role=role,
    )

    ct = ContentType.objects.get_for_model(device)
    placement = ObjectPlacement.objects.create(
        floor_plan=floorplan1,
        content_type=ct,
        object_id=device.pk,
        x=100,
        y=200,
        color="#0d6efd",
    )
    return placement
