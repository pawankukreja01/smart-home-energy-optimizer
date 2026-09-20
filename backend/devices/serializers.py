from rest_framework import serializers
from .models import (
    Device,
    EnergyReading,
    AutomationAction,
    EnergySaving,
)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "device_type",
            "room",
            "is_on",
            "power_watts",
            "created_at",
        ]


class EnergyReadingSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(
        source="device.name",
        read_only=True
    )

    class Meta:
        model = EnergyReading
        fields = [
            "id",
            "device",
            "device_name",
            "power_watts",
            "timestamp",
        ]


class AutomationActionSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(
        source="device.name",
        read_only=True
    )

    class Meta:
        model = AutomationAction
        fields = [
            "id",
            "device",
            "device_name",
            "action_type",
            "reason",
            "power_before",
            "power_after",
            "potential_saving_watts",
            "timestamp",
        ]
        
class EnergySavingSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(
        source="device.name",
        read_only=True
    )

    class Meta:
        model = EnergySaving
        fields = [
            "id",
            "device",
            "device_name",
            "automation_action",
            "power_saved_watts",
            "duration_hours",
            "energy_saved_kwh",
            "estimated_cost_saved",
            "timestamp",
            "ended_at",
        ]
