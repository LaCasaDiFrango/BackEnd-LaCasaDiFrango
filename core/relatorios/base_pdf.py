from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
import io

def gerar_relatorio_base(titulo, colunas, dados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    # Cabeçalho com logo
    try:
        logo = Image("core/static/logo.png", width=80, height=40)
        elementos.append(logo)
    except:
        pass
    elementos.append(Paragraph(titulo, styles["Title"]))
    elementos.append(Paragraph(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    elementos.append(Spacer(1, 20))

    # Tabela de dados
    tabela = Table([colunas] + dados)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    elementos.append(tabela)

    # Rodapé simples
    elementos.append(Spacer(1, 30))
    elementos.append(Paragraph("Sistema de Relatórios — La Casa Di Frango", styles["Italic"]))

    doc.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
