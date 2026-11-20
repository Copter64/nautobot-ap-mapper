"""Django API urlpatterns declaration for ap_mapper app."""

from nautobot.apps.api import OrderedDefaultRouter

from ap_mapper.api import views

router = OrderedDefaultRouter()
router.register("floor-plans", views.APFloorPlanViewSet)
router.register("placements", views.ObjectPlacementViewSet)

app_name = "ap_mapper-api"
urlpatterns = router.urls
