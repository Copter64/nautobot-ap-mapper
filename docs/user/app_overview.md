# App Overview

This document provides an overview of the App including critical information and important considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

AP Mapper provides interactive floor plan mapping for wireless access points and network devices within Nautobot. The app allows network engineers to:

- Upload floor plan images (PNG/JPEG/SVG) for sites and locations
- Drag and drop access points, devices, racks, and other network objects onto the map
- View placement markers with colors, labels, and coordinates
- Manage floor plans per location with revision tracking

The app integrates into the Nautobot UI with a "Wireless" tab in the sidebar and adds AP Map tabs to Device and Location detail pages.

## Audience (User Personas) - Who should use this App?

- **Network Engineers**: Visualize wireless AP placement and coverage during planning and troubleshooting
- **Site Engineers**: Document physical device locations on floor plans
- **NOC Operators**: Quickly identify device locations for field dispatch
- **Nautobot Administrators**: Extend Nautobot with visual mapping capabilities

## Authors and Maintainers

- **Copter64** (Chris Sibiski) — Primary author and maintainer

## Nautobot Features Used

AP Mapper integrates with the following Nautobot features:

- **DCIM**: Location, Device, Rack models
- **Wireless**: WirelessAP model
- **Extras**: Tags, Custom Fields (via PrimaryModel base)
- **Content Types**: GenericForeignKey for flexible object placement

### Extras

- **Custom Fields**: No custom fields are created by this app. It uses the standard Nautobot PrimaryModel base which supports tags and custom fields natively.
- **Jobs**: No jobs are installed by this app.
