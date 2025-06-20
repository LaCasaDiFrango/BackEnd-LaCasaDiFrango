from rest_framework.viewsets import ModelViewSet

from core.models.usuario.endereco import Endereco
from core.serializers.usuario.endereco import EnderecoSerializer, EnderecoRetrieveSerializer

class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    def get_serializer_class(self):
        if self.action == "retrieve":
            return EnderecoRetrieveSerializer
        return EnderecoSerializer