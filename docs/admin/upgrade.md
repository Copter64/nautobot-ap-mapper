# Upgrading the App

Here you will find any steps necessary to upgrade the App in your Nautobot environment.

## Upgrade Guide

To upgrade AP Mapper, update the package and run migrations:

1. Upgrade the package:

```shell
pip install --upgrade ap-mapper
```

2. Run the post-upgrade command to apply any database migrations and clear cache:

```shell
nautobot-server post_upgrade
```

3. Restart Nautobot services if necessary:

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

When a new release comes out it may be necessary to run a migration of the database to account for any changes in the data models used by this app. The `post_upgrade` command handles this automatically.
