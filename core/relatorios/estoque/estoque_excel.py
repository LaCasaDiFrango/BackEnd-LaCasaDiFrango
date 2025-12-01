import openpyxl
from django.http import HttpResponse
from core.models.produto.produto import Produto


def relatorio_estoque_excel(request):
    # Cria o workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estoque"

    # Cabeçalhos
    ws.append([
        "ID",
        "Nome",
        "Preço",
        "Descrição",
        "Quantidade em Estoque",
        "Categoria"
    ])

    # Dados
    produtos = Produto.objects.select_related("categoria").all()

    for p in produtos:
        ws.append([
            p.id,
            p.nome,
            float(p.preco),
            p.descricao,
            p.quantidade_em_estoque,
            p.categoria.nome if p.categoria else "Sem categoria"
        ])

    # Preparar resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename="relatorio_estoque.xlsx"'

    wb.save(response)
    return response
