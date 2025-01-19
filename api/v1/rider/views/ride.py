from ..serializer import RideSerializer
from rest_framework.viewsets import ModelViewSet
from ride.models import Ride
from helpers.permissions import IsRider
from rest_framework.permissions import IsAuthenticated
from rider.config.response import SuccessResponse, ErrorResponse
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RideViewSet(ModelViewSet):
    """
    Ride ViewSet
    """

    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsRider]

    @swagger_auto_schema(
        operation_description="Update ride status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Ride status",
                    enum=[
                        "REQUESTED",
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
            ride.save()
            return SuccessResponse(message="Ride status updated successfully")
        return ErrorResponse(message="Invalid status")

    def get_queryset(self):
        return Ride.objects.filter(rider=self.request.user).order_by(
            "-created_at"
        )

    def get_serializer_context(self):
        return {"user": self.request.user}
