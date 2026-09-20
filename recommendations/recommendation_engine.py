def generate_recommendation(device_name, power_watts):
    if device_name == "Living Room AC" and power_watts > 1000:
        excess_power = power_watts - 1000

        return {
            "type": "energy_anomaly",
            "device": device_name,
            "message": (
                f"Abnormally high AC consumption detected: "
                f"{power_watts}W."
            ),
            "recommendation": (
                "Reduce AC load or inspect the unit for "
                "abnormal power consumption."
            ),
            "potential_saving_watts": round(excess_power, 2),
        }

    if device_name == "Bedroom TV" and 0 < power_watts < 20:
        return {
            "type": "standby_energy",
            "device": device_name,
            "message": (
                f"TV is consuming {power_watts}W while "
                "apparently inactive."
            ),
            "recommendation": (
                "Consider switching the TV completely off "
                "to eliminate standby consumption."
            ),
            "potential_saving_watts": round(power_watts, 2),
        }

    return None