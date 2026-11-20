"""Template extensions for AP Mapper."""

from nautobot.apps.ui import MenuChooseAction, TemplateExtension


class DeviceAPMapTab(TemplateExtension):
    """Add an 'AP Map' tab to the Device detail view."""

    model = "dcim.device"

    object_detail_tabs = [
        MenuChooseAction(
            tab_id="ap-map",
            label="AP Map",
            menu=(
                {
                    "link": "plugins:ap_mapper:device_ap_map",
                    "label": "View on Map",
                    "weight": 100,
                    "button_class": "btn-primary",
                    "required_permissions": ["ap_mapper.view_apfloorplan"],
                },
            ),
            weight=800,
        )
    ]


class LocationAPMapTab(TemplateExtension):
    """Add an 'AP Map' tab to the Location detail view."""

    model = "dcim.location"

    object_detail_tabs = [
        MenuChooseAction(
            tab_id="ap-map",
            label="AP Map",
            menu=(
                {
                    "link": "plugins:ap_mapper:location_ap_map",
                    "label": "View on Map",
                    "weight": 100,
                    "button_class": "btn-primary",
                    "required_permissions": ["ap_mapper.view_apfloorplan"],
                },
            ),
            weight=800,
        )
    ]


template_extensions = [DeviceAPMapTab, LocationAPMapTab]
