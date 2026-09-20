import os
import sys

import requests
import pandas as pd
from sklearn.ensemble import IsolationForest

# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BACKEND_PATH = os.path.join(
    PROJECT_ROOT,
    "backend"
)

# Allow Python to find the Django project
sys.path.insert(0, BACKEND_PATH)

# Allow imports from the project root
sys.path.insert(0, PROJECT_ROOT)


# --------------------------------------------------
# Project imports
# --------------------------------------------------

from recommendations.recommendation_engine import (
    generate_recommendation
)

from automation.automation_engine import (
    switch_device_off
)


# --------------------------------------------------
# API configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000/api/energy-readings/"


# --------------------------------------------------
# Normal energy ranges
# --------------------------------------------------

NORMAL_RANGES = {
    "Living Room AC": (700, 1000),
    "Living Room Light": (20, 60),
    "Bedroom TV": (60, 150),
    "Kitchen Light": (20, 60),
}


# --------------------------------------------------
# Get energy readings
# --------------------------------------------------

def get_energy_readings():
    response = requests.get(
        API_URL,
        params={"limit": 30}
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# Detect anomalies
# --------------------------------------------------

def detect_anomalies():

    readings = get_energy_readings()

    if len(readings) < 10:
        print("Not enough data for anomaly detection.")
        return

    df = pd.DataFrame(readings)

    print()
    print("🤖 AI ENERGY ANALYSIS")
    print("---------------------")

    anomalies_found = False

    # Analyze each device separately
    for device_name, device_data in df.groupby("device_name"):

        # Ignore devices without a defined normal range
        if device_name not in NORMAL_RANGES:
            continue

        minimum, maximum = NORMAL_RANGES[device_name]

        device_data = device_data.copy()

        # --------------------------------------------------
        # Check whether readings are outside normal range
        # --------------------------------------------------

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

        # --------------------------------------------------
        # AI anomaly detection
        # --------------------------------------------------

        if len(device_data) >= 5:

            X = device_data[["power_watts"]]

            model = IsolationForest(
                contamination=0.1,
                random_state=42
            )

            device_data["prediction"] = model.fit_predict(X)

            anomalies = device_data[
                (device_data["outside_range"])
                &
                (device_data["prediction"] == -1)
            ]

        else:
            anomalies = unusual_data

        # --------------------------------------------------
        # Process detected anomalies
        # --------------------------------------------------

        for _, row in anomalies.iterrows():

            anomalies_found = True

            power = float(row["power_watts"])

            print(
                f"🚨 {device_name}: "
                f"{power:.2f}W "
                f"(AI anomaly detected)"
            )

            # --------------------------------------------------
            # Generate recommendation
            # --------------------------------------------------

            recommendation = generate_recommendation(
                device_name,
                power
            )

            if recommendation:

                potential_saving = (
                    recommendation[
                        "potential_saving_watts"
                    ]
                )

                print(
                    "💡 Recommendation: "
                    f"{recommendation['recommendation']}"
                )

                print(
                    "⚡ Potential saving: "
                    f"{potential_saving:.2f}W"
                )

                # --------------------------------------------------
                # Automated response
                # --------------------------------------------------

                if (
                    device_name == "Living Room AC"
                    and power > 1000
                ):

                    automation_result = switch_device_off(
                        device_name=device_name,
                        power_before=power,
                        potential_saving_watts=potential_saving,
                        reason=recommendation[
                            "recommendation"
                        ],
                    )

                    print(
                        automation_result["message"]
                    )

    # --------------------------------------------------
    # No anomalies
    # --------------------------------------------------

    if not anomalies_found:

        print(
            "✅ No unusual energy consumption detected."
        )


# --------------------------------------------------
# Run detector
# --------------------------------------------------

if __name__ == "__main__":
    detect_anomalies()