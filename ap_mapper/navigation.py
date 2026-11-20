"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

floor_plan_items = (
    NavMenuItem(
        link="plugins:ap_mapper:apfloorplan_list",
        name="Floor Plans",
        permissions=["ap_mapper.view_apfloorplan"],
        buttons=(
            NavMenuAddButton(
                link="plugins:ap_mapper:apfloorplan_add",
                permissions=["ap_mapper.add_apfloorplan"],
            ),
        ),
    ),
)

placement_items = (
    NavMenuItem(
        link="plugins:ap_mapper:objectplacement_list",
        name="Placements",
        permissions=["ap_mapper.view_objectplacement"],
        buttons=(
            NavMenuAddButton(
                link="plugins:ap_mapper:objectplacement_add",
                permissions=["ap_mapper.add_objectplacement"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Wireless",
        groups=(
            NavMenuGroup(name="AP Mapper", items=floor_plan_items),
            NavMenuGroup(name="Map Objects", items=placement_items),
        ),
    ),
)
