"""Template extensions for AP Mapper."""

from nautobot.apps.ui import DistinctViewTab, TemplateExtension


class DeviceAPMapTab(TemplateExtension):
    """Add an 'AP Map' tab to the Device detail view."""

    # pylint: disable=abstract-method
    model = "dcim.device"

    object_detail_tabs = [
        DistinctViewTab(
            tab_id="ap-map",
            label="AP Map",
            url_name="plugins:ap_mapper:device_ap_map",
            weight=800,
            required_permissions=["ap_mapper.view_apfloorplan"],
        )
    ]


class LocationAPMapTab(TemplateExtension):
    """Add an 'AP Map' tab to the Location detail view."""

    # pylint: disable=abstract-method
    model = "dcim.location"

    object_detail_tabs = [
        DistinctViewTab(
            tab_id="ap-map",
            label="AP Map",
            url_name="plugins:ap_mapper:location_ap_map",
            weight=800,
            required_permissions=["ap_mapper.view_apfloorplan"],
        )
    ]


template_extensions = [DeviceAPMapTab, LocationAPMapTab]
