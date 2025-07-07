from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from core.models.usuario.endereco import Endereco
from core.serializers.usuario.endereco import EnderecoSerializer, EnderecoRetrieveSerializer

class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EnderecoRetrieveSerializer
        return EnderecoSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            # Admin vê todos os endereços
            return Endereco.objects.all()
        # Usuário comum vê apenas os próprios endereços
        return Endereco.objects.filter(usuario=user)
