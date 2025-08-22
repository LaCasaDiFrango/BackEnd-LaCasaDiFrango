from django.contrib.auth.models import Group

def sync_user_groups(user):
    """
    Sincroniza grupos do Django com o perfil do usuário.
    Remove grupos antigos e adiciona o grupo correto baseado no perfil.
    """
    perfil_to_group = {
        'administrador': 'administradores',
        'vendedor': 'vendedores',
        'usuario': 'usuarios',
    }

    # Remove todos os grupos atuais
    user.groups.clear()

    # Adiciona grupo conforme perfil
    group_name = perfil_to_group.get(user.perfil)
    if group_name:
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            # Opcional: logar aviso
            pass
