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
import matplotlib.pyplot as plt
import io

from core.models.usuario.user import User

# Fonte compatível com acentuação
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))


# -----------------------------------------------------
# Função auxiliar para gerar gráficos e retornar como imagem
# -----------------------------------------------------
def gerar_grafico_pizza(ativos, inativos):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(
        [ativos, inativos],
        labels=['Ativos', 'Inativos'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['#1f77b4', '#ff7f0e']
    )
    ax.set_title('Distribuição de Usuários')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer


def gerar_grafico_barras_top_usuarios():
    usuarios = (
        User.objects
        .annotate(total_pedidos=models.Count('pedidos'))
        .order_by('-total_pedidos')[:5]
    )
    nomes = [u.name or '—' for u in usuarios]
    valores = [u.total_pedidos for u in usuarios]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.barh(nomes, valores, color='#004080')
    ax.set_title('Top 5 Usuários com Mais Pedidos')
    ax.set_xlabel('Total de Pedidos')
    ax.invert_yaxis()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer


def gerar_grafico_linha_crescimento():
    """Simula crescimento com base na quantidade de usuários ativos/inativos por mês."""
    hoje = timezone.now()
    meses = [(hoje - timedelta(days=30 * i)).strftime("%b/%y") for i in reversed(range(6))]
    contagens = []

    for i in reversed(range(6)):
        inicio = hoje - timedelta(days=30 * (i + 1))
        fim = hoje - timedelta(days=30 * i)
        # usa ultimo_pedido como proxy de atividade
        count = User.objects.filter(ultimo_pedido__gte=inicio, ultimo_pedido__lt=fim).count()
        contagens.append(count)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(meses, contagens, marker='o', color='#0066cc')
    ax.set_title('Atividade de Usuários nos Últimos 6 Meses')
    ax.set_ylabel('Usuários com Pedido')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer


# -----------------------------------------------------
# Função principal de geração do PDF
# -----------------------------------------------------
def gerar_relatorio_usuarios(request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Relatório de Usuários - La Casa Di Frango")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Resumo", fontSize=11, leading=14))
    styles.add(ParagraphStyle(name="Indicador", fontSize=14, leading=18, alignment=1))
    elements = []

    # -----------------------------------------------------
    # CAPA
    # -----------------------------------------------------
    try:
        logo = Image("core/static/logo.png", width=150, height=80)
        logo.hAlign = 'CENTER'
        elements.append(logo)
    except Exception:
        pass

    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<b>Relatório de Usuários</b>", styles["Title"]))
    elements.append(Paragraph("Sistema de Gestão — La Casa Di Frango", styles["Normal"]))
    elements.append(Spacer(1, 15))

    nome_responsavel = request.user.name if request and hasattr(request, 'user') else "Administrador"
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")

    elements.append(Paragraph(f"Responsável: <b>{nome_responsavel}</b>", styles["Normal"]))
    elements.append(Paragraph(f"Data de emissão: {data_geracao}", styles["Normal"]))
    elements.append(Spacer(1, 50))
    elements.append(PageBreak())

    # -----------------------------------------------------
    # RESUMO GERAL
    # -----------------------------------------------------
    total = User.objects.count()
    ativos = User.objects.filter(is_active=True).count()
    inativos = User.objects.filter(is_active=False).count()

    hoje = timezone.now()
    limite = hoje - timedelta(days=30)
    novos_mes = User.objects.filter(last_login__gte=limite).count()
    mes_passado = User.objects.filter(last_login__lt=limite, last_login__gte=limite - timedelta(days=30)).count()

    crescimento = ((novos_mes - mes_passado) / mes_passado * 100) if mes_passado > 0 else 0
    media_pedidos = round(User.objects.aggregate(media=models.Avg('pedidos__id'))['media'] or 0, 1)

    elements.append(Paragraph("<b>Resumo Geral</b>", styles["Heading2"]))
    resumo = [
        ["Total", "Ativos", "Inativos", "Usuários Ativos no Mês", "Variação %", "Média Pedidos"],
        [total, ativos, inativos, novos_mes, f"{crescimento:.1f}%", media_pedidos]
    ]
    t = Table(resumo, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'HeiseiMin-W3'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, 1), colors.whitesmoke),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 25))

    # -----------------------------------------------------
    # GRÁFICOS
    # -----------------------------------------------------
    elements.append(Paragraph("<b>Gráficos</b>", styles["Heading2"]))

    grafico_pizza = gerar_grafico_pizza(ativos, inativos)
    elements.append(Image(grafico_pizza, width=200, height=150))
    elements.append(Spacer(1, 10))

    grafico_barras = gerar_grafico_barras_top_usuarios()
    elements.append(Image(grafico_barras, width=250, height=180))
    elements.append(Spacer(1, 10))

    grafico_linha = gerar_grafico_linha_crescimento()
    elements.append(Image(grafico_linha, width=300, height=180))
    elements.append(PageBreak())

    # -----------------------------------------------------
    # TABELA DETALHADA
    # -----------------------------------------------------
    elements.append(Paragraph("<b>Lista Detalhada de Usuários</b>", styles["Heading2"]))
    colunas = ["ID", "Nome", "Email", "Ativo", "Perfil", "Último Pedido", "Último Login"]
    dados = []

    for user in User.objects.all().order_by('id'):
        ultimo_pedido = (
            timezone.localtime(user.ultimo_pedido).strftime('%d/%m/%Y %H:%M')
            if user.ultimo_pedido else "—"
        )
        ultimo_login = (
            timezone.localtime(user.last_login).strftime('%d/%m/%Y %H:%M')
            if user.last_login else "—"
        )
        dados.append([
            user.id,
            user.name or "—",
            user.email,
            "Sim" if user.is_active else "Não",
            user.get_perfil_display(),
            ultimo_pedido,
            ultimo_login
        ])

    tabela = Table([colunas] + dados, hAlign='LEFT', repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'HeiseiMin-W3'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))
    elements.append(tabela)
    elements.append(PageBreak())

    # -----------------------------------------------------
    # RODAPÉ INSTITUCIONAL
    # -----------------------------------------------------
    elements.append(Paragraph(
        """
        <b>La Casa Di Frango — Sistema de Relatórios</b><br/>
        © 2025 Todos os direitos reservados.<br/>
        Política de Privacidade: os dados seguem as diretrizes da LGPD.<br/>
        www.lacasadifrango.com.br
        """,
        styles["Italic"]
    ))

    # -----------------------------------------------------
    # Geração final do PDF
    # -----------------------------------------------------
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# -----------------------------------------------------
# View REST
# -----------------------------------------------------
def relatorio_usuarios(request):
    pdf = gerar_relatorio_usuarios(request)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_usuarios.pdf"'
    return response
