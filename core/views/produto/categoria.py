from rest_framework.viewsets import ModelViewSet

from core.models.produto.categoria import Categoria
from core.serializers.produto.categoria import CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer