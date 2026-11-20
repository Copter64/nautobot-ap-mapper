# Getting Started with the App

This document provides a step-by-step tutorial on how to get the App going and how to use it.

## Install the App

To install the App, please follow the instructions detailed in the [Installation Guide](../admin/install.md).

## First steps with the App

1. **Create a Floor Plan**: Navigate to the "Wireless" tab in the Nautobot sidebar, then select "Floor Plans" → "Add". Choose a Location, upload a floor plan image (PNG/JPEG/SVG), and set the logical dimensions (e.g., 1000x1000 for a 1000px wide image).

2. **View the Map**: Open the floor plan detail page to see the interactive map. You can pan and zoom the floor plan image.

3. **Place Objects**: Click the "Edit Map" button, then "Add Object". Select an object type (WirelessAP, Device, Rack, etc.) and an object instance. Drag the marker to the desired position on the floor plan.

4. **Save**: Click "Save" to persist the placements. The revision counter increments with each save.

## What are the next steps?

- Add multiple access points to a floor plan to visualize coverage
- Use different marker colors to distinguish between AP types or statuses
- Add labels to markers for quick identification
- Create floor plans for multiple floors/locations in your site
- Use the REST API to automate placement creation from external systems

You can check out the [Use Cases](app_use_cases.md) section for more examples.
