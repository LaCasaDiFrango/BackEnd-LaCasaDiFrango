from django.http import HttpResponse
from core.relatorios.base_pdf import gerar_relatorio_base
from core.models.produto.produto import Produto

def relatorio_estoque(request):
    colunas = ["ID", "Produto", "Categoria", "Qtd Atual", "Qtd Mínima", "Valor Unitário (R$)"]
    dados = [
        [
            p.id,
            p.nome,
            p.categoria.nome if p.categoria else "-",
            p.quantidade,
            p.quantidade_minima,
            f"{p.valor_unitario:.2f}" if hasattr(p, "valor_unitario") else "-"
        ]
        for p in Produto.objects.all().order_by('nome')
    ]

    pdf = gerar_relatorio_base("Relatório de Estoque", colunas, dados)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_estoque.pdf"'
    return response
