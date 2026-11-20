# External Interactions

This document describes external dependencies and prerequisites for this App to operate.

## External System Integrations

AP Mapper has **no external system dependencies**. It operates entirely within Nautobot:

- Floor plan images are stored as Nautobot static files
- Object placements reference existing Nautobot models (DCIM, Wireless)
- No external API calls, databases, or services are required

### From the App to Other Systems

None. The app does not call external APIs or services.

### From Other Systems to the App

External systems can interact with AP Mapper via the Nautobot REST API endpoints listed below.

## Nautobot REST API endpoints

AP Mapper exposes the following REST API endpoints under `/api/plugins/ap-mapper/`:

- **Floor Plans**: `/api/plugins/ap-mapper/floor-plans/`
  - `GET`: List all floor plans (supports filtering by location)
  - `POST`: Create a new floor plan
  - `GET /<pk>/`: Get a specific floor plan
  - `PUT /<pk>/`: Update a floor plan
  - `PATCH /<pk>/`: Partially update a floor plan
  - `DELETE /<pk>/`: Delete a floor plan and its placements

- **Object Placements**: `/api/plugins/ap-mapper/object-placements/`
  - `GET`: List all placements (supports filtering by floor_plan, content_type)
  - `POST`: Create a new placement
  - `GET /<pk>/`: Get a specific placement
  - `PUT /<pk>/`: Update a placement (coordinates, color, label)
  - `PATCH /<pk>/`: Partially update a placement
  - `DELETE /<pk>/`: Delete a placement

### Example: Create a placement via curl

```bash
curl -X POST \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "floor_plan": 1,
    "content_type": "dcim.device",
    "object_id": 42,
    "x": 500,
    "y": 300,
    "color": "#0d6efd",
    "label": "AP-Floor1-North"
  }' \
  http://nautobot.example.com/api/plugins/ap-mapper/object-placements/
```
