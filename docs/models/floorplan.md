# Floor Plan

The `APFloorPlan` model represents a floor plan map for a Nautobot Location. Each location can have one floor plan.

## Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `location` | ForeignKey to `dcim.Location` | The location this floor plan belongs to. Immutable after creation. |
| `background` | FileField | The floor plan image file (PNG/JPEG/SVG). |
| `logical_width` | PositiveIntegerField | Logical width of the map in pixels (1–10000). |
| `logical_height` | PositiveIntegerField | Logical height of the map in pixels (1–10000). |
| `revision` | PositiveIntegerField | Revision counter. Increments automatically on each update. |
| `name` | CharField | Optional name for the floor plan. Falls back to location name if empty. |
| `description` | CharField | Optional description. |

## Constraints

- One floor plan per location (unique constraint on `location`)
- `logical_width` and `logical_height` must be between 1 and 10000
- `revision` must be >= 1
- `location` is immutable after creation (enforced in `clean()`)
