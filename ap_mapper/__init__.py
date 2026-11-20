"""App declaration for ap_mapper."""

from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class APMapperConfig(NautobotAppConfig):
    """App configuration for the ap_mapper app."""

    name = "ap_mapper"
    verbose_name = "AP Mapper"
    version = __version__
    author = "Chris Sibiski"
    description = "Wireless AP mapping with floor plan visualization for Nautobot."
    base_url = "ap-mapper"
    required_settings = []
    default_settings = {
        "supported_targets": [
            "wireless.wirelessap",
            "dcim.device",
            "dcim.rack",
            "dcim.location",
        ],
        "marker_default_color": "#0d6efd",
        "marker_size": 30,
        "background_max_bytes": 5_000_000,
        "background_max_dimension": 10000,
    }
    docs_view_name = "plugins:ap_mapper:docs"
    searchable_models = ["apfloorplan", "objectplacement"]


config = APMapperConfig  # pylint:disable=invalid-name
