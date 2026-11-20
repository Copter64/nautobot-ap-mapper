# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Initial release of AP Mapper for Nautobot
- Provides interactive floor plan mapping for wireless access points and network devices
- Compatible with Nautobot 3.1.0 and later

## [v1.0.0] - 2026-11-20

### Added

- `APFloorPlan` model: Upload floor plan images per location with logical dimensions and revision tracking
- `ObjectPlacement` model: Place any Nautobot object (WirelessAP, Device, Rack, etc.) on a floor plan using GenericForeignKey
- Interactive Leaflet.js map with drag-and-drop placement
- Full REST API for floor plans and placements
- UI integration: "Wireless" tab in Nautobot sidebar
- AP Map tabs on Device and Location detail pages
- Color-coded markers with labels and custom colors
- Filters, forms, and tables for floor plans and placements
- Unit tests for models, views, API, filters, and forms
- GitHub Actions CI workflow for linting and documentation checks
