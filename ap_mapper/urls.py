"""Django urlpatterns declaration for ap_mapper app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from ap_mapper import views

app_name = "ap_mapper"
router = NautobotUIViewSetRouter()

# Floor plans
router.register("floor-plans", views.APFloorPlanUIViewSet)
# Object placements
router.register("placements", views.ObjectPlacementUIViewSet)

# Custom map views
urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("ap_mapper/docs/index.html")), name="docs"),
    # Floor plan interactive map
    path("floor-plans/<uuid:pk>/map/", views.FloorPlanMapView.as_view(), name="apfloorplan_map"),
    # Location-scoped map (finds the map for a location)
    path("location/<uuid:location_pk>/map/", views.FloorPlanMapView.as_view(), name="location_ap_map"),
    # Device-scoped map (finds the map containing this device)
    path("device/<uuid:device_pk>/map/", views.DeviceMapView.as_view(), name="device_ap_map"),
]

urlpatterns += router.urls
