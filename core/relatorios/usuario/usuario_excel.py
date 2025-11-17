import openpyxl
from django.http import HttpResponse
from django.utils import timezone
from core.models.usuario.user import User


def relatorio_usuarios_excel(request):
    wb = openpyxl.Workbook()    
    ws = wb.active
    ws.title = "Usuários"

    # Cabeçalhos
    ws.append([
        "ID",
        "Email",
        "Nome",
        "Perfil",
        "Está Ativo?",
        "É Staff?",
        "Endereço",
        "Último Pedido"
    ])

    usuarios = User.objects.select_related("endereco").all()

    for u in usuarios:
        # Formata data do último pedido
        if u.ultimo_pedido:
            ultimo = timezone.localtime(u.ultimo_pedido).strftime("%Y-%m-%d %H:%M")
        else:
            ultimo = "—"

        ws.append([
            u.id,
            u.email,
            u.name or "",
            u.get_perfil_display(),
            "Sim" if u.is_active else "Não",
            "Sim" if u.is_staff else "Não",
            str(u.endereco) if u.endereco else "Sem endereço",
            ultimo,
        ])

    # HTTP Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="relatorio_usuarios.xlsx"'

    wb.save(response)
    return response
