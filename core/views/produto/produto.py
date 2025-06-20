from rest_framework.viewsets import ModelViewSet

from core.models.produto.produto import Produto
from core.serializers.produto.produto import ProdutoSerializer, ProdutoListSerializer, ProdutoRetrieveSerializer

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return ProdutoListSerializer
        elif self.action == "retrieve":
            return ProdutoRetrieveSerializer
        return ProdutoSerializer