from django.urls import path

from core.relatorios.usuario.usuario_pdf import relatorio_usuarios
from core.relatorios.usuario.usuario_excel import relatorio_usuarios_excel

from core.relatorios.estoque.estoque_pdf import relatorio_estoque
from core.relatorios.estoque.estoque_excel import relatorio_estoque_excel

from core.relatorios.pedido.pedido_pdf import relatorio_pedidos
from core.relatorios.pedido.pedido_excel import export_pedido_excel


urlpatterns = [
    path('relatorios/usuarios/pdf/', relatorio_usuarios, name='relatorio_usuarios_pdf'),
    path('relatorios/usuarios/excel/', relatorio_usuarios_excel, name='relatorio_usuarios_excel'),

    path('relatorios/estoque/pdf/', relatorio_estoque, name='relatorio_estoque_pdf'),
    path('relatorios/estoque/excel/', relatorio_estoque_excel, name='relatorio_estoque_excel'),

    path('relatorios/pedidos/pdf/', relatorio_pedidos, name='relatorio_pedidos_pdf'),
    path('relatorios/pedidos/excel/', export_pedido_excel, name='relatorio_pedidos_excel'),

]

