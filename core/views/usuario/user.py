from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from core.permissions import IsAdminUser, IsOwnerOrAdmin
from core.models.usuario.user import User
from core.serializers.usuario.user import UserSerializer, UserListSerializer
from app.pagination import CustomPagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

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
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def ativos_inativos(self, request):
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

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def mais_ativos(self, request):
        """
        Retorna os top 10 usuários com mais pedidos
        """
        usuarios = (
            User.objects
            .annotate(total_pedidos=Count('pedidos'))  # 'pedidos' vem do related_name do Pedido
            .order_by('-total_pedidos')[:10]
        )
        data = [
            {'id': u.id, 'name': u.name, 'total_pedidos': u.total_pedidos}
            for u in usuarios
        ]
        return Response(data, status=status.HTTP_200_OK)
