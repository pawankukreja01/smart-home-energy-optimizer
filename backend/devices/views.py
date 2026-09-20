from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

import os
import sys

from django.utils import timezone

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

import pandas as pd
from sklearn.ensemble import IsolationForest

from .models import (
    Device,
    EnergyReading,
    AutomationAction,
    EnergySaving,
)

from .serializers import (
    DeviceSerializer,
    EnergyReadingSerializer,
    AutomationActionSerializer,
    EnergySavingSerializer,
)

from recommendations.recommendation_engine import (
    generate_recommendation
)


# Electricity price used for estimated savings.
# This is a configurable example rate.
ELECTRICITY_RATE_PER_KWH = 0.30


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def perform_update(self, serializer):

        # Capture the device state before the update
        device = self.get_object()

        was_on = device.is_on

        # Save the requested device update
        updated_device = serializer.save()

        is_now_on = updated_device.is_on

        # ---------------------------------------------------------
        # If a device has been turned ON, close any active
        # energy-saving period associated with that device.
        # ---------------------------------------------------------
        if not was_on and is_now_on:

            active_saving = (
                EnergySaving.objects
                .filter(
                    device=updated_device,
                    ended_at__isnull=True
                )
                .order_by("-timestamp")
                .first()
            )

            if active_saving:

                ended_at = timezone.now()

                duration_seconds = (
                    ended_at - active_saving.timestamp
                ).total_seconds()

                duration_hours = (
                    duration_seconds / 3600
                )

                energy_saved_kwh = (
                    active_saving.power_saved_watts
                    * duration_hours
                ) / 1000

                estimated_cost_saved = (
                    energy_saved_kwh
                    * ELECTRICITY_RATE_PER_KWH
                )

                active_saving.ended_at = ended_at

                active_saving.duration_hours = round(
                    duration_hours,
                    4
                )

                active_saving.energy_saved_kwh = round(
                    energy_saved_kwh,
                    4
                )

                active_saving.estimated_cost_saved = round(
                    estimated_cost_saved,
                    4
                )

                active_saving.save(
                    update_fields=[
                        "ended_at",
                        "duration_hours",
                        "energy_saved_kwh",
                        "estimated_cost_saved",
                    ]
                )


class EnergyReadingViewSet(viewsets.ModelViewSet):
    serializer_class = EnergyReadingSerializer

    def get_queryset(self):
        limit = self.request.query_params.get(
            "limit",
            30
        )

        try:
            limit = int(limit)
        except ValueError:
            limit = 30

        return (
            EnergyReading.objects
            .all()
            .order_by("-timestamp")[:limit]
        )


# Expected normal operating ranges for each device
NORMAL_RANGES = {
    "Living Room AC": (700, 1000),
    "Living Room Light": (20, 60),
    "Bedroom TV": (60, 150),
    "Kitchen Light": (20, 60),
}


@api_view(["GET"])
def analytics(request):

    readings = (
        EnergyReading.objects
        .select_related("device")
        .order_by("-timestamp")[:30]
    )

    # No readings available
    if not readings:
        return Response({
            "alert_count": 0,
            "latest_anomaly": None,
            "recommendation": None,
            "potential_saving_watts": 0,
        })

    data = []

    for reading in readings:
        data.append({
            "device_name": reading.device.name,
            "power_watts": reading.power_watts,
            "timestamp": reading.timestamp,
        })

    df = pd.DataFrame(data)

    anomalies = []

    # Analyze each device separately
    for device_name, device_data in df.groupby(
        "device_name"
    ):

        if device_name not in NORMAL_RANGES:
            continue

        minimum, maximum = NORMAL_RANGES[
            device_name
        ]

        device_data = device_data.copy()

        # Check whether readings are outside
        # the expected operating range
        device_data["outside_range"] = (
            (device_data["power_watts"] < minimum)
            |
            (device_data["power_watts"] > maximum)
        )

        unusual_data = device_data[
            device_data["outside_range"]
        ]

        if unusual_data.empty:
            continue

        # Use Isolation Forest to confirm unusual patterns
        if len(device_data) >= 5:

            model = IsolationForest(
                contamination=0.1,
                random_state=42
            )

            X = device_data[["power_watts"]]

            device_data["prediction"] = (
                model.fit_predict(X)
            )

            detected = device_data[
                (device_data["outside_range"])
                &
                (device_data["prediction"] == -1)
            ]

        else:
            detected = unusual_data

        # Create anomaly information
        for _, row in detected.iterrows():

            recommendation = generate_recommendation(
                device_name,
                row["power_watts"]
            )

            anomalies.append({
                "device": device_name,
                "power_watts": float(
                    row["power_watts"]
                ),
                "normal_min_watts": minimum,
                "normal_max_watts": maximum,
                "timestamp": row["timestamp"],
                "recommendation": (
                    recommendation["recommendation"]
                    if recommendation
                    else None
                ),
                "potential_saving_watts": (
                    recommendation[
                        "potential_saving_watts"
                    ]
                    if recommendation
                    else 0
                ),
            })

    # Newest anomaly first
    anomalies.sort(
        key=lambda item: item["timestamp"],
        reverse=True
    )

    latest_anomaly = (
        anomalies[0]
        if anomalies
        else None
    )

    return Response({
        "alert_count": len(anomalies),

        "latest_anomaly": latest_anomaly,

        "recommendation": (
            latest_anomaly["recommendation"]
            if latest_anomaly
            else None
        ),

        "potential_saving_watts": (
            latest_anomaly[
                "potential_saving_watts"
            ]
            if latest_anomaly
            else 0
        ),
    })


@api_view(["GET"])
def energy_history(request):

    readings = (
        EnergyReading.objects
        .select_related("device")
        .order_by("-timestamp")[:50]
    )

    data = []

    for reading in reversed(readings):

        data.append({
            "device_name": reading.device.name,
            "power_watts": reading.power_watts,
            "timestamp": reading.timestamp,
        })

    return Response(data)


@api_view(["GET"])
def automation_history(request):

    actions = (
        AutomationAction.objects
        .select_related("device")
        .order_by("-timestamp")[:20]
    )

    serializer = AutomationActionSerializer(
        actions,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
def energy_savings(request):

    savings = (
        EnergySaving.objects
        .select_related("device", "automation_action")
        .order_by("-timestamp")[:20]
    )

    serializer = EnergySavingSerializer(
        savings,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
def energy_savings_analytics(request):

    savings = EnergySaving.objects.all()

    total_energy_saved = sum(
        saving.energy_saved_kwh
        for saving in savings
    )

    total_cost_saved = sum(
        saving.estimated_cost_saved
        for saving in savings
    )

    total_power_avoided = sum(
        saving.power_saved_watts
        for saving in savings
    )

    completed_savings = savings.filter(
        ended_at__isnull=False
    )

    return Response({
        "total_energy_saved_kwh": round(
            total_energy_saved,
            4
        ),

        "total_cost_saved": round(
            total_cost_saved,
            4
        ),

        "total_power_avoided_watts": round(
            total_power_avoided,
            2
        ),

        "automation_actions": savings.count(),

        "completed_savings": completed_savings.count(),

        "active_savings": savings.filter(
            ended_at__isnull=True
        ).count(),
    })