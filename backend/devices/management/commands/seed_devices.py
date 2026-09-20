from django.core.management.base import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = "Create the default Smart Home demo devices"

    def handle(self, *args, **options):
        devices = [
            {
                "name": "Living Room Light",
                "device_type": "light",
                "room": "Living Room",
                "is_on": True,
                "power_watts": 40,
            },
            {
                "name": "Living Room AC",
                "device_type": "ac",
                "room": "Living Room",
                "is_on": True,
                "power_watts": 850,
            },
            {
                "name": "Bedroom TV",
                "device_type": "tv",
                "room": "Bedroom",
                "is_on": False,
                "power_watts": 0,
            },
            {
                "name": "Kitchen Light",
                "device_type": "light",
                "room": "Kitchen",
                "is_on": False,
                "power_watts": 0,
            },
        ]

        for device_data in devices:
            device, created = Device.objects.update_or_create(
                name=device_data["name"],
                defaults=device_data,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {device.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Already exists: {device.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Default Smart Home devices are ready."
            )
        )
