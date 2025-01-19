from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from helpers.permissions import IsDriver
from ..serializer import DriverRideSerializer
from ride.models import Ride
from rider.config.response import SuccessResponse, ErrorResponse
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import math
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import ACos, Cos, Radians, Sin


class DriverRideViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsDriver]
    serializer_class = DriverRideSerializer
    queryset = Ride.objects.all().order_by("-created_at")

    @action(methods=["get"], detail=False, url_path="my-rides")
    def my_rides(self, request):
        queryset = Ride.objects.filter(driver=request.user).order_by(
            "-created_at"
        )
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_description="Update ride status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Ride status",
                    enum=[
                        "ACCEPTED",
                        "IN_PROGRESS",
                        "COMPLETED",
                        "CANCELLED",
                    ],
                )
            },
        ),
    )
    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        ride = self.get_object()
        status = request.data.get("status")
        if status in dict(Ride.RideStatus.choices):
            ride.status = status
            if status == Ride.RideStatus.ACCEPTED:
                if ride.driver is not None:
                    return ErrorResponse(message="Ride already accepted")
                ride.driver = request.user
            elif ride.driver != request.user:
                return ErrorResponse(message="Unauthorized", status_code=403)

            ride.save()
            return SuccessResponse(message="Ride status updated successfully")
        return ErrorResponse(message="Invalid status")

    @action(detail=False, methods=["list"])
    def list_rides(self, request, *args, **kwargs):
        if not self.request.user.lat or not self.request.user.long:
            data = self.get_serializer(
                self.get_queryset().filter(driver__isnull=True), many=True
            ).data
            return SuccessResponse(data=data)

        user_lat = self.request.user.lat
        user_lon = self.request.user.long
        queryset = (
            super()
            .get_queryset().filter(driver__isnull=True)
            .annotate(
                distance=ExpressionWrapper(
                    6371
                    * ACos(
                        Cos(Radians(user_lat))
                        * Cos(Radians(F("pickup_location_lat")))
                        * Cos(
                            Radians(F("pickup_location_lon"))
                            - Radians(user_lon)
                        )
                        + Sin(Radians(user_lat))
                        * Sin(Radians(F("pickup_location_lat")))
                    ),
                    output_field=FloatField(),
                )
            )
            .order_by("distance")
        )

        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points on the earth
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        return c * 6371
