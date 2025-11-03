from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from core.permissions import IsAdminUser, IsOwnerOrAdmin
from core.models.usuario.user import User
from core.serializers.usuario.user import UserSerializer, UserListSerializer
from app.pagination import CustomPagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtros e pesquisa
    filterset_fields = ['is_active', 'groups__name']
    search_fields = ['name', 'email']
    ordering_fields = ['id', 'name', 'email', 'ultimo_pedido']
    ordering = ['id']

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action == 'list':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retorna os dados do próprio usuário"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def ativos_inativos(self, request):
        """
        Retorna contagem de usuários ativos e inativos.
        Usuário ativo: último pedido nos últimos 30 dias
        Usuário inativo: último pedido há mais de 30 dias ou nunca fez pedido
        """
        hoje = timezone.localtime(timezone.now())
        limite = hoje - timedelta(days=30)

        queryset = self.get_queryset()
        ativos = 0
        inativos = 0

        for user in queryset:
            if user.ultimo_pedido:
                ultimo_local = timezone.localtime(user.ultimo_pedido)
                if ultimo_local >= limite:
                    ativos += 1
                else:
                    inativos += 1
            else:
                inativos += 1

        return Response({
        "ativos": ativos,
        "inativos": inativos
        }, status=status.HTTP_200_OK)

