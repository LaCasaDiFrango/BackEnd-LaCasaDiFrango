import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.db import models
import io

from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto

pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))


# ==========================================================
# PALETA VISUAL
# ==========================================================
HEADER_COLOR = colors.HexColor("#003366")    # Azul marinho
ACCENT_COLOR = colors.HexColor("#0050A0")    # Azul de destaque
LIGHT_BG     = colors.HexColor("#F5F7FA")    # Cinza claro
WHITE        = colors.white
GREY         = colors.grey


# ==========================================================
# GRÁFICO: STATUS
# ==========================================================
def grafico_status():
    stats = (
        Pedido.objects
        .values("status")
        .annotate(total=models.Count("id"))
    )

    labels = []
    valores = []

    for s in stats:
        labels.append(Pedido.StatusCompra(s["status"]).label)
        valores.append(s["total"])

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(valores, labels=labels, autopct="%1.1f%%", startangle=90)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ==========================================================
# GRÁFICO: FATURAMENTO 6 MESES
# ==========================================================
def grafico_faturamento_6m():
    hoje = timezone.now()
    meses = [(hoje - timedelta(days=30 * i)).strftime("%b/%y") for i in reversed(range(6))]

    valores = []
    for i in reversed(range(6)):
        inicio = hoje - timedelta(days=30 * (i + 1))
        fim = hoje - timedelta(days=30 * i)
        total = (
            Pedido.objects
            .filter(data_criacao__gte=inicio, data_criacao__lt=fim)
            .aggregate(s=models.Sum("total"))
        )["s"] or 0
        valores.append(total)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(meses, valores, marker="o")
    ax.set_title("Faturamento últimos 6 meses")
    ax.set_ylabel("R$ total")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ==========================================================
# RELATÓRIO
# ==========================================================
def gerar_relatorio_pedidos(request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Relatório de Pedidos")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Resumo", fontSize=11, leading=14))
    elements = []

    # CAPA
    try:
        logo = Image("core/static/logo.png", width=150, height=80)
        logo.hAlign = "CENTER"
        elements.append(logo)
    except:
        pass

    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<b>Relatório de Pedidos</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    resp = getattr(request.user, "name", "Administrador") if request else "Administrador"
    elements.append(Paragraph(f"Responsável: {resp}", styles["Normal"]))
    elements.append(
        Paragraph(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"])
    )
    elements.append(PageBreak())

    # RESUMO
    total = Pedido.objects.count()
    concluidos = Pedido.objects.filter(status=Pedido.StatusCompra.ENTREGUE).count()
    faturamento_total = Pedido.objects.aggregate(models.Sum("total"))["total__sum"] or 0

    elements.append(Paragraph("<b>Resumo Geral</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    resumo = [
        ["Métrica", "Valor"],
        ["Pedidos Totais", total],
        ["Pedidos Entregues", concluidos],
        ["Faturamento Total", f"R$ {faturamento_total:,.2f}"],
    ]

    t = Table(resumo, hAlign="LEFT", colWidths=[150, 200])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_COLOR),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "HeiseiMin-W3"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),

                ("GRID", (0, 0), (-1, -1), 0.5, GREY),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
                ("FONTNAME", (0, 1), (-1, -1), "HeiseiMin-W3"),
            ]
        )
    )

    elements.append(t)
    elements.append(Spacer(1, 20))


    # GRÁFICOS
    elements.append(Paragraph("<b>Gráficos</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    pizza = grafico_status()
    elements.append(Paragraph("Status dos pedidos", styles["Normal"]))
    elements.append(Image(pizza, width=220, height=160))
    elements.append(Spacer(1, 12))

    linha = grafico_faturamento_6m()
    elements.append(Paragraph("Faturamento últimos 6 meses", styles["Normal"]))
    elements.append(Image(linha, width=340, height=200))
    elements.append(PageBreak())


    # TABELA DETALHADA
    elements.append(Paragraph("<b>Pedidos Detalhados</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    cols = ["ID", "Cliente", "Status", "Valor", "Criado em"]
    dados = []

    for p in Pedido.objects.all().order_by("id"):
        dados.append(
            [
                p.id,
                getattr(p.usuario, "name", "—"),
                p.get_status_display(),
                f"R$ {p.total:,.2f}",
                p.data_criacao.strftime("%d/%m/%Y %H:%M") if p.data_criacao else "—",
            ]
        )

    tabela = Table([cols] + dados, repeatRows=1, colWidths=[40, 120, 90, 80, 120])

    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_COLOR),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "HeiseiMin-W3"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),

                ("GRID", (0, 0), (-1, -1), 0.25, GREY),
                ("FONTNAME", (0, 1), (-1, -1), "HeiseiMin-W3"),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
            ]
        )
    )

    elements.append(tabela)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def relatorio_pedidos(request):
    pdf = gerar_relatorio_pedidos(request)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="relatorio_pedidos.pdf"'
    return response
