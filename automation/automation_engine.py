import os
import sys
from datetime import timezone

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BACKEND_PATH = os.path.join(
    PROJECT_ROOT,
    "backend"
)

sys.path.insert(0, BACKEND_PATH)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

import django

django.setup()

import requests

from devices.models import (
    AutomationAction,
    EnergySaving,
)


API_URL = "http://127.0.0.1:8000/api/devices/"

ELECTRICITY_RATE_PER_KWH = 0.30


def calculate_savings(
    power_saved_watts,
    duration_hours
):
    energy_saved_kwh = (
        power_saved_watts * duration_hours
    ) / 1000

    estimated_cost_saved = (
        energy_saved_kwh
        * ELECTRICITY_RATE_PER_KWH
    )

    return {
        "energy_saved_kwh": round(
            energy_saved_kwh,
            4
        ),
        "estimated_cost_saved": round(
            estimated_cost_saved,
            4
        ),
    }


def switch_device_off(
    device_name,
    power_before=0,
    potential_saving_watts=0,
    reason="Abnormal energy consumption detected."
):
    response = requests.get(API_URL)
    response.raise_for_status()

    devices = response.json()

    for device in devices:

        if device["name"] == device_name:

            if not device["is_on"]:
                return {
                    "success": True,
                    "message": f"{device_name} is already OFF.",
                    "action_recorded": False,
                    "saving_recorded": False,
                }

            update_response = requests.patch(
                f"{API_URL}{device['id']}/",
                json={
                    "is_on": False,
                    "power_watts": 0,
                }
            )

            update_response.raise_for_status()

            automation_action = AutomationAction.objects.create(
                device_id=device["id"],
                action_type="DEVICE_SWITCHED_OFF",
                reason=reason,
                power_before=power_before,
                power_after=0,
                potential_saving_watts=potential_saving_watts,
            )

            EnergySaving.objects.create(
                device_id=device["id"],
                automation_action=automation_action,
                power_saved_watts=potential_saving_watts,
                duration_hours=0,
                energy_saved_kwh=0,
                estimated_cost_saved=0,
            )

            return {
                "success": True,
                "message": (
                    f"🤖 Automation: "
                    f"{device_name} switched OFF."
                ),
                "action_recorded": True,
                "saving_recorded": True,
            }

    return {
        "success": False,
        "message": f"Device '{device_name}' not found.",
        "action_recorded": False,
        "saving_recorded": False,
    }


def calculate_energy_saving(
    saving_id,
    duration_hours
):
    try:
        saving = EnergySaving.objects.get(
            id=saving_id
        )
    except EnergySaving.DoesNotExist:
        return {
            "success": False,
            "message": (
                f"EnergySaving record "
                f"{saving_id} not found."
            ),
        }

    savings = calculate_savings(
        saving.power_saved_watts,
        duration_hours
    )

    saving.duration_hours = duration_hours

    saving.energy_saved_kwh = (
        savings["energy_saved_kwh"]
    )

    saving.estimated_cost_saved = (
        savings["estimated_cost_saved"]
    )

    saving.save(
        update_fields=[
            "duration_hours",
            "energy_saved_kwh",
            "estimated_cost_saved",
        ]
    )

    return {
        "success": True,
        "saving_id": saving.id,
        "power_saved_watts": saving.power_saved_watts,
        "duration_hours": saving.duration_hours,
        "energy_saved_kwh": saving.energy_saved_kwh,
        "estimated_cost_saved": (
            saving.estimated_cost_saved
        ),
    }