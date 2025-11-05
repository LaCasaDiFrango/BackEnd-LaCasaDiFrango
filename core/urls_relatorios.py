from django.urls import path
from core.relatorios.usuario.usuario_pdf import relatorio_usuarios
from core.relatorios.estoque.estoque_pdf import relatorio_estoque
from core.relatorios.pedido.pedido_pdf import relatorio_pedidos

urlpatterns = [
    path('relatorios/usuarios/pdf/', relatorio_usuarios, name='relatorio_usuarios_pdf'),
    path('relatorios/estoque/pdf/', relatorio_estoque, name='relatorio_estoque_pdf'),
    path('relatorios/pedidos/pdf/', relatorio_pedidos, name='relatorio_pedidos_pdf'),
]
