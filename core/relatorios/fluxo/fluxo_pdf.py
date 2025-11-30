#from django.http import HttpResponse
#from core.relatorios.base_pdf import gerar_relatorio_base
#from core.models.financeiro.movimentacao import Movimentacao  # ajuste o caminho do model se diferente

#def relatorio_fluxo_caixa(request):
 #   colunas = ["Data", "Tipo", "Descrição", "Categoria", "Valor (R$)"]
  #  dados = [
   #     [
    #        m.data.strftime("%d/%m/%Y %H:%M"),
     #       m.tipo.capitalize(),
      #      m.descricao,
       #     m.categoria.nome if hasattr(m, "categoria") else "-",
    #        f"{m.valor:.2f}"
     #   ]
      #  for m in Movimentacao.objects.all().order_by('-data')
  #  ]

  #  pdf = gerar_relatorio_base("Relatório de Fluxo de Caixa", colunas, dados)
   # response = HttpResponse(pdf, content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="relatorio_fluxo_caixa.pdf"'
   # return response
