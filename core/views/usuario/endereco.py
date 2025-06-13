from rest_framework.viewsets import ModelViewSet

from core.models.usuario.endereco import Endereco
from core.serializers.usuario.endereco import EnderecoSerializer

class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer