# Extending the App

AP Mapper is designed to be extensible. The following approaches are supported:

## Adding New Object Types

To support additional object types (beyond WirelessAP, Device, Rack, Location), update the `supported_targets` setting in `PLUGINS_CONFIG`:

```python
PLUGINS_CONFIG = {
    "ap_mapper": {
        "supported_targets": [
            "wireless.wirelessap",
            "dcim.device",
            "dcim.rack",
            "dcim.location",
            "virtualization.virtualmachine",  # Add your type here
        ],
    },
}
```

The `ObjectPlacement` model uses a GenericForeignKey, so any Nautobot model can be placed on a map without code changes.

## Custom Marker Styles

Marker colors are stored per placement. To add custom color palettes or default styles, modify the `marker_default_color` setting or extend the JavaScript in `ap_mapper/static/ap_mapper/js/ap_mapper.js`.

## Contributing Changes

Extending the application is welcome, however it is best to open an issue first, to ensure that a PR would be accepted and makes sense in terms of features and design.
