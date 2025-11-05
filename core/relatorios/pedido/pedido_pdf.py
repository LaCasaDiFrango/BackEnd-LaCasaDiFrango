from django.http import HttpResponse
from core.relatorios.base_pdf import gerar_relatorio_base
from core.models.pedido.pedido import Pedido

def relatorio_pedidos(request):
    colunas = ["ID", "Usuário", "Data Pedido", "Status", "Valor Total (R$)"]
    dados = [
        [
            p.id,
            p.usuario.nome if hasattr(p, "usuario") else "-",
            p.data_pedido.strftime("%d/%m/%Y %H:%M") if p.data_pedido else "-",
            p.status,
            f"{p.valor_total:.2f}" if hasattr(p, "valor_total") else "-"
        ]
        for p in Pedido.objects.all().order_by('-data_pedido')
    ]

    pdf = gerar_relatorio_base("Relatório de Pedidos", colunas, dados)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_pedidos.pdf"'
    return response
