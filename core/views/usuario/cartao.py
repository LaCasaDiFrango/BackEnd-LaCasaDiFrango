from rest_framework.viewsets import ModelViewSet

from core.models.usuario.cartao import Cartao
from core.serializers.usuario.cartao import CartaoSerializer

class CartaoViewSet(ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer