# relatorios/pedido/excel/pedido_excel.py
from django.http import HttpResponse
from core.relatorios.base_excel import BaseExcelReport
from core.models.pedido.pedido import Pedido


class PedidoExcelReport(BaseExcelReport):
    sheet_name = "Pedidos"

    def __init__(self):
        queryset = Pedido.objects.select_related("usuario").all()
        fields = [
            "id",
            "usuario__name",          # se o User tiver campo "nome"
            "status",
            "total",
            "data_criacao",
            "data_de_retirada",
        ]
        super().__init__(queryset, fields)

    def get_dataframe(self):
        df = super().get_dataframe()

    # Converter status numérico → texto
        df["status"] = df["status"].apply(
            lambda s: Pedido.StatusCompra(s).label
        )

    # Remover timezone dos campos datetime (Excel exige tz-unaware)
        if "data_criacao" in df.columns:
            df["data_criacao"] = df["data_criacao"].dt.tz_localize(None)

        if "data_de_retirada" in df.columns:
            df["data_de_retirada"] = df["data_de_retirada"].dt.tz_localize(None)

        return df



def export_pedido_excel(request):
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="pedidos.xlsx"'

    return PedidoExcelReport().render(response)
