from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..serializer import RiderSerializer
from helpers.permissions import IsRider


class RiderViewSet(ModelViewSet):
    serializer_class = RiderSerializer
    http_method_names = ["get", "post", "put", "patch"]

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action == "create":
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, IsRider]
        return [permission() for permission in permission_classes]
