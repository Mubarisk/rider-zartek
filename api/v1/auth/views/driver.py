from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..serializer import DriverSerializer
from helpers.permissions import IsDriver


class DriverViewSet(ModelViewSet):
    serializer_class = DriverSerializer
    http_method_names = ["get", "post", "put", "patch"]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, IsDriver]
        return [permission() for permission in permission_classes]

    def get_object(self):
        return self.request.user