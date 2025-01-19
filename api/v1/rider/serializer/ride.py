from rest_framework import serializers
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):
    """
    Ride Serializer
    """

    class Meta:
        model = Ride
        exclude = (
            "created_at",
            "updated_at",
            "rider",
        )
        read_only_fields = (
            "id",
            "status",
            "driver",
            "current_location_lat",
            "current_location_lon",
        )

    def create(self, validated_data):
        return Ride.objects.create(
            rider=self.context["user"], **validated_data
        )
