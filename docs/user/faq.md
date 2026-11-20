# Frequently Asked Questions

## What file formats are supported for floor plans?

PNG, JPEG, and SVG images are supported. We recommend PNG for lossless quality or SVG for scalable vector graphics.

## Can I place any Nautobot object on a map?

Yes. The app uses a GenericForeignKey, so any Nautobot model can be placed. By default, WirelessAP, Device, Rack, and Location are supported. You can add more types via the `supported_targets` configuration setting.

## What happens if I move or delete a Location?

Floor plans are linked to Locations. If you delete a Location that has a floor plan, the floor plan and all its placements will be deleted (cascading delete). Moving a Location is not currently supported — floor plans are immutable with respect to their location.

## Can I have multiple floor plans per Location?

No. Each Location can have at most one floor plan. This enforces a clear 1:1 relationship between a physical location and its map.

## How are coordinates stored?

Placements are stored as pixel coordinates (x, y) relative to the top-left corner of the floor plan image. The `logical_width` and `logical_height` fields define the coordinate space. Coordinates are validated to be within bounds (0 to logical_width-1, 0 to logical_height-1).

## Can I use this with Nautobot 2.x?

No. AP Mapper requires Nautobot 3.1.0 or later. It uses 3.x APIs and features.

## How do I bulk-import placements?

Use the REST API. You can create multiple placements via `POST /api/plugins/ap-mapper/object-placements/` in a script or automation tool. See the [External Interactions](external_interactions.md) page for API examples.
