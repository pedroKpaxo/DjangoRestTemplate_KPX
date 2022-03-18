from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils.translation import gettext_lazy as _  # noqa
from apps.user.permissions import IsAuthenticatedAndTechnical, IsAuthenticatedAndExecutive
from shared.viewsets import CreateListRetrieveViewSet
from rest_framework.generics import RetrieveUpdateAPIView

from .models import TechnicalUser, ExecutiveUser, AcademicUser
from . import serializers


class TechnicalUserViewSet(CreateListRetrieveViewSet):
    queryset = TechnicalUser.objects.all()
    serializer_class = serializers.TechnicalUserSerializer
    permission_classes = [IsAuthenticatedAndTechnical]
    ordering = ['-created_at']
    filterset_fields = ['is_active', 'type']
    search_fields = ['name', 'email']
    ordering_fields = ['created_at', 'name']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedAndTechnical])
    def deactivate(self, request, pk=None):
        """Update the user's status to active."""
        user = self.get_object()
        current_status = user.is_active
        if current_status is True:
            user.deactivate()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                "detail": _(f"Não é possível desativar o usuário {user.get_full_name()},"
                            " pois este já se encontra inativo")
            }, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedAndTechnical])
    def activate(self, request, pk=None):
        """Update the user's status to active."""
        user = self.get_object()
        current_status = user.is_active
        if current_status is False:
            user.activate()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                "detail": _(f"Não é possível ativar o usuário {user.get_full_name()},"
                            " pois este já se encontra ativo")
            }, status=status.HTTP_400_BAD_REQUEST
        )
