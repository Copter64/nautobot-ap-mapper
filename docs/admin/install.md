# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The app is compatible with Nautobot 3.1.0 and higher.
- Databases supported: PostgreSQL, MySQL
- Python 3.10 or higher

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

### Access Requirements

AP Mapper has no external system dependencies. It operates entirely within Nautobot using existing models (Location, Device, Rack, WirelessAP) and stores floor plan images as static files.

## Install Guide

The app is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install ap-mapper
```

Or from source:

```shell
git clone https://github.com/Copter64/nautobot-ap-mapper.git
cd nautobot-ap-mapper
pip install -e .
```

To ensure AP Mapper is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `ap-mapper` package:

```shell
echo ap-mapper >> local_requirements.txt
```

Once installed, the app needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"ap_mapper"` to the `PLUGINS` list.
- Append the `"ap_mapper"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["ap_mapper"]

# PLUGINS_CONFIG = {
#   "ap_mapper": {
#     ADD YOUR SETTINGS HERE
#   }
# }
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration

The app behavior can be controlled with the following list of settings:

| Key | Example | Default | Description |
| --- | ------- | ------- | ----------- |
| `supported_targets` | `["wireless.wirelessap", "dcim.device", "dcim.rack", "dcim.location"]` | `["wireless.wirelessap", "dcim.device", "dcim.rack", "dcim.location"]` | List of content types that can be placed on maps. Format: `app_label.model_name`. |
| `marker_default_color` | `"#0d6efd"` | `"#0d6efd"` | Default color for placement markers (hex color). |
| `marker_size` | `30` | `30` | Default marker size in pixels. |
