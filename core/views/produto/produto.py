from rest_framework.viewsets import ModelViewSet

from core.models.produto.produto import Produto
from core.serializers.produto.produto import ProdutoSerializer

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer