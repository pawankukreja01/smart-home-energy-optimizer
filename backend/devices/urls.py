from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DeviceViewSet,
    EnergyReadingViewSet,
    analytics,
    energy_history,
    automation_history,
    energy_savings,
    energy_savings_analytics,
)

router = DefaultRouter()

router.register(
    "devices",
    DeviceViewSet,
    basename="device"
)

router.register(
    "energy-readings",
    EnergyReadingViewSet,
    basename="energy-reading"
)

urlpatterns = [
    path("analytics/", analytics),
    path("energy-history/", energy_history),
    path("automation-history/", automation_history),
    path("energy-savings/", energy_savings),
    path(
        "energy-savings-analytics/",
        energy_savings_analytics
    ),
]
urlpatterns += router.urls