from rest_framework import serializers
from ride.models import Ride


class DriverRideSerializer(serializers.ModelSerializer):
    """
    Ride Serializer
    """

    class Meta:
        model = Ride
        exclude = ("driver",)
