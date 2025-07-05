from rest_framework.viewsets import ModelViewSet

from core.models.produto.produto import Produto
from core.serializers.produto.produto import ProdutoSerializer, ProdutoListSerializer, ProdutoRetrieveSerializer, ProdutoAlterarPrecoSerializer

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return ProdutoListSerializer
        elif self.action == "retrieve":
            return ProdutoRetrieveSerializer
        return ProdutoSerializer

    @action(detail=True, methods=['patch'])
    def alterar_preco(self, request, pk=None):
        produto = self.get_object()

        serializer = ProdutoAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        produto.preco = serializer.validated_data['preco']
        produto.save()

        return Response(
            {'detail': f'Preço do produto "{produto.titulo}" atualizado para {produto.preco}.'}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def ajustar_estoque(self, request, pk=None):
        produto = self.get_object()

        serializer = ProdutoAjustarEstoqueSerializer(data=request.data, context={'produto': produto})
        serializer.is_valid(raise_exception=True)

        quantidade_ajuste = serializer.validated_data['quantidade_em_estoque']

        produto.quantidade_em_estoque += quantidade_ajuste
        produto.save()

        return Response(
            {'status': 'Quantidade ajustada com sucesso', 'novo_estoque': produto.quantidade_em_estoque}, status=status.HTTP_200_OK
        )