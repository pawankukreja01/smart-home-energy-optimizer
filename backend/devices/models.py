from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    room = models.CharField(max_length=100)

    is_on = models.BooleanField(default=False)

    power_watts = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EnergyReading(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="energy_readings"
    )

    power_watts = models.FloatField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.device.name} - "
            f"{self.power_watts}W"
        )


class AutomationAction(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="automation_actions"
    )

    action_type = models.CharField(
        max_length=50
    )

    reason = models.TextField()

    power_before = models.FloatField(
        default=0
    )

    power_after = models.FloatField(
        default=0
    )

    potential_saving_watts = models.FloatField(
        default=0
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.device.name} - "
            f"{self.action_type}"
        )


class EnergySaving(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="energy_savings"
    )

    automation_action = models.ForeignKey(
        AutomationAction,
        on_delete=models.CASCADE,
        related_name="energy_savings"
    )

    power_saved_watts = models.FloatField(default=0)

    duration_hours = models.FloatField(default=0)

    energy_saved_kwh = models.FloatField(default=0)

    estimated_cost_saved = models.FloatField(default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.device.name} - "
            f"{self.energy_saved_kwh:.3f} kWh saved"
        )