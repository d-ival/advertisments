from advertisements.filters import AdvertisementFilter, AdvertismentFilterBackend
from advertisements.models import Advertisement,AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

class AdvertisementPermission(permissions.BasePermission):
    """Обеспечивает проверку прав на изменение или удаление объекта"""

    def has_object_permission(self, request, view, obj):
        modify_methods = ('PATCH', 'PUT', 'DELETE')
        if request.method in modify_methods or obj.status == AdvertisementStatusChoices.DRAFT:
            return request.user == obj.creator
        return True

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    permission_classes = [AdvertisementPermission & IsAuthenticatedOrReadOnly]
    queryset = Advertisement.objects.all()

    filter_backends = [AdvertismentFilterBackend]
    filterset_class = AdvertisementFilter
    serializer_class = AdvertisementSerializer




    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ["create", "update", "partial_update"]:
    #         return [IsAuthenticated()]
    #     return []
