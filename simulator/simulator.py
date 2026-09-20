import os
import random
import time
import requests


API_URL = "http://127.0.0.1:8000/api/energy-readings/"


DEVICE_PROFILES = {
    "light": {
        "normal": (20, 60),
    },
    "ac": {
        "normal": (700, 1000),
    },
    "tv": {
        "normal": (60, 150),
    },
    "thermostat": {
        "normal": (2, 5),
    },
    "appliance": {
        "normal": (300, 1200),
    },
}


def generate_power(device):
    profile = DEVICE_PROFILES.get(
        device["device_type"],
        {"normal": (10, 100)}
    )

    minimum, maximum = profile["normal"]

    if not device["is_on"]:
        return 0

    # Demo mode: deliberately create an AC anomaly
# Demo mode: deliberately create an AC anomaly
    if (
        os.getenv("DEMO_MODE") == "1"
        and device["device_type"] == "ac"
    ):
        return round(random.uniform(1500, 1800), 2)

    # Normal operation
    if device["device_type"] == "ac" and random.random() < 0.10:
        return round(random.uniform(1400, 1800), 2)

    return round(random.uniform(minimum, maximum), 2)

def get_devices():
    response = requests.get(
        "http://127.0.0.1:8000/api/devices/"
    )

    response.raise_for_status()

    return response.json()


def send_reading(device, power):
    payload = {
        "device": device["id"],
        "power_watts": power,
    }

    response = requests.post(
        API_URL,
        json=payload,
    )

    response.raise_for_status()

    return response.json()


def main():
    print("🏠 Smart Home IoT Simulator Started")
    print("------------------------------------")

    while True:
        devices = get_devices()

        for device in devices:
            power = generate_power(device)

            reading = send_reading(
                device,
                power,
            )

            print(
                f"📡 {device['name']}: "
                f"{power}W"
            )

        print("------------------------------------")

        time.sleep(5)


if __name__ == "__main__":
    main()