from django.db import models
from user.models import User

# Create your models here.


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        ACCEPTED = "ACCEPTED", "Accepted"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    rider = models.ForeignKey(
        User, related_name="rides", on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        User,
        related_name="driven_rides",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=RideStatus.choices, default=RideStatus.REQUESTED
    )
    current_location_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    current_location_lon = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
