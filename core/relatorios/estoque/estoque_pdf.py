import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from django.http import HttpResponse
from datetime import datetime
import io

from django.db import models
from core.models.produto.produto import Produto

# Font for unicode support
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# ---------------------------------------------------------------
# PALETA E ESTILOS
# ---------------------------------------------------------------
PRIMARY = colors.HexColor("#003366")
PRIMARY_LIGHT = colors.HexColor("#335C85")
ACCENT = colors.HexColor("#007ACC")
DANGER = colors.HexColor("#C62828")
GREY = colors.HexColor("#EEEEEE")
TEXT_FADE = colors.HexColor("#555555")


def grafico_estoque_baixo():
    """Top 5 produtos com menor estoque."""
    produtos = Produto.objects.order_by("quantidade_em_estoque")[:5]
    nomes = [p.nome for p in produtos]
    qts = [p.quantidade_em_estoque for p in produtos]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.barh(nomes, qts)
    ax.set_title("Top 5: Menor Estoque")
    ax.invert_yaxis()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ---------------------------------------------------------------
# RELATÓRIO
# ---------------------------------------------------------------
def gerar_relatorio_estoque(request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()

    # custom styles
    h1 = ParagraphStyle(
        'H1',
        parent=styles['Title'],
        fontSize=22,
        textColor=PRIMARY,
        spaceAfter=12
    )
    h2 = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=6
    )
    body = styles["Normal"]

    elements = []

    # CAPA -------------------------------------------------------
    try:
        logo = Image("core/static/logo.png", width=170, height=90)
        logo.hAlign = 'CENTER'
        elements.append(logo)
    except:
        pass

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Relatório de Estoque</b>", h1))
    elements.append(Paragraph(
        f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        body
    ))

    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", color=PRIMARY, thickness=2))
    elements.append(PageBreak())

    # RESUMO -----------------------------------------------------
    total = Produto.objects.count()

    elements.append(Paragraph("<b>Resumo</b>", h2))

    resumo = [
        ["Total Produtos"],
        [total]
    ]

    resumo_table = Table(resumo, colWidths=[120])
    resumo_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.4, GREY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GREY, colors.white]),
    ]))

    elements.append(resumo_table)
    elements.append(Spacer(1, 20))

    # GRÁFICO ----------------------------------------------------
    graf = grafico_estoque_baixo()
    elements.append(Paragraph("<b>Top 5 - Menor Estoque</b>", h2))
    elements.append(Image(graf, width=300, height=170))
    elements.append(PageBreak())

    # TABELA DETALHADA -------------------------------------------
    elements.append(Paragraph("<b>Estoque Detalhado</b>", h2))

    cols = ["ID", "Nome", "Qtd. Estoque", "Categoria"]
    dados = [
        [
            p.id,
            p.nome,
            p.quantidade_em_estoque,
            p.categoria.nome if p.categoria else "—",
        ]
        for p in Produto.objects.all().order_by("id")
    ]

    tabela = Table([cols] + dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),

        ("GRID", (0, 0), (-1, -1), 0.3, GREY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GREY]),
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
    ]))

    elements.append(tabela)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def relatorio_estoque(request):
    pdf = gerar_relatorio_estoque(request)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename=\"relatorio_estoque.pdf\"'
    return response
