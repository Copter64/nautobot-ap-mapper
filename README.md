# AP Mapper

<p align="center">
  <img src="https://raw.githubusercontent.com/Copter64/nautobot-ap-mapper/main/docs/images/icon-ap-mapper.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/Copter64/nautobot-ap-mapper/actions"><img src="https://github.com/Copter64/nautobot-ap-mapper/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

AP Mapper provides interactive floor plan mapping for wireless access points and network devices within Nautobot. The app allows network engineers to upload floor plan images for sites and locations, then drag and drop access points, devices, racks, and other network objects onto the map for visual placement.

Key features:

- **Floor Plan Management**: Upload floor plan images (PNG/JPEG/SVG) per location with configurable logical dimensions and revision tracking
- **Interactive Map**: Leaflet.js-powered map with drag-and-drop placement of network objects
- **Flexible Object Support**: Place any Nautobot object type — WirelessAPs, Devices, Racks, or custom types — via GenericForeignKey
- **Visual Markers**: Color-coded markers with labels and custom colors for easy identification
- **API Support**: Full REST API for creating, updating, and querying floor plans and placements
- **UI Integration**: Adds a "Wireless" tab to the Nautobot sidebar and AP Map tabs on Device and Location detail pages

The app is designed for wireless network planning and troubleshooting — quickly see where your access points are physically located, identify coverage gaps, and visualize network topology on a per-floor basis.

## Documentation

Full documentation for this App can be found in the [docs folder](https://github.com/Copter64/nautobot-ap-mapper/tree/main/docs):

- [User Guide](https://github.com/Copter64/nautobot-ap-mapper/tree/main/docs/user) - Overview, Getting Started, Use Cases, FAQ.
- [Administrator Guide](https://github.com/Copter64/nautobot-ap-mapper/tree/main/docs/admin) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://github.com/Copter64/nautobot-ap-mapper/tree/main/docs/dev) - Extending the App, Code Reference, Development Environment, Contribution Guide.
- [Release Notes](https://github.com/Copter64/nautobot-ap-mapper/tree/main/docs/admin/release_notes).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/Copter64/nautobot-ap-mapper/tree/main/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://github.com/Copter64/nautobot-ap-mapper/blob/main/docs/dev/dev_environment.md)). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Installation

Quick install via Poetry:

```bash
poetry add ap-mapper
```

Or from source:

```bash
git clone https://github.com/Copter64/nautobot-ap-mapper.git
cd nautobot-ap-mapper
pip install -e .
```

Add `ap_mapper` to your Nautobot `PLUGINS` list and run `python nautobot-server migrate`. See the [Installation Guide](https://github.com/Copter64/nautobot-ap-mapper/blob/main/docs/admin/install.md) for full details.

## Questions

For any questions or comments, please check the [FAQ](https://github.com/Copter64/nautobot-ap-mapper/blob/main/docs/user/faq.md) first. Feel free to also open an issue on the [GitHub repository](https://github.com/Copter64/nautobot-ap-mapper/issues).
