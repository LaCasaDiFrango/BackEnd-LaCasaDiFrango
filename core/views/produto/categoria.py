from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser, IsGuestOrReadOnly
from rest_framework.viewsets import ModelViewSet

from core.models.produto.categoria import Categoria
from core.serializers.produto.categoria import CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ['list', 'retrieve']:
            return [IsGuestOrReadOnly()]
        return super().get_permissions()
