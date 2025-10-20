from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from core.permissions import IsAdminUser
from core.models.usuario.endereco import Endereco
from core.serializers.usuario.endereco import EnderecoSerializer, EnderecoRetrieveSerializer
from app.pagination import CustomPagination


class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['usuario__id', 'cidade', 'estado', 'cep']
    search_fields = ['rua', 'bairro', 'cidade', 'estado']
    ordering_fields = ['id', 'cidade', 'estado']
    ordering = ['id']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EnderecoRetrieveSerializer
        return EnderecoSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        """Usuário comum vê só os próprios endereços; admin vê todos."""
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='administradores').exists():
            return Endereco.objects.all()
        return Endereco.objects.filter(usuario=user)
