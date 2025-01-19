from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from helpers.permissions import IsDriver
from ..serializer import DriverRideSerializer
from ride.models import Ride
from rider.config.response import SuccessResponse, ErrorResponse
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DriverRideViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsDriver]
    serializer_class = DriverRideSerializer
    queryset = Ride.objects.all()

    @action(methods=["get"], detail=False)
    def list_rides(self, request):
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
                return ErrorResponse(message="Unauthorized")

            ride.save()
            return SuccessResponse(message="Ride status updated successfully")
        return ErrorResponse(message="Invalid status")
