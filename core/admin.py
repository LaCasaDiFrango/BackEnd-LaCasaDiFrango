"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models.usuario.user import User
from core.models.usuario.endereco import Endereco
from core.models.usuario.cartao import Cartao
from core.models.produto.produto import Produto
from core.models.produto.categoria import Categoria
from core.models.pedido.pedido import Pedido
from core.models.pedido.item_pedido import ItemPedido
from core.models.pagamento.pagamento import Pagamento
from core.models.pagamento.metodo_de_pagamento import MetodoDePagamento


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'bairro', 'rua', 'numero', 'cep')
    search_fields = ('bairro', 'rua', 'numero', 'cep')
    list_filter = ('bairro',)

@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    list_display = ('numero_cartao', 'nome_titular', 'data_de_validade')
    search_fields = ('numero_cartao', 'nome_titular')
    list_filter = ('data_de_validade',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade_em_estoque')
    search_fields = ('nome',)
    list_filter = ('categoria',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    search_fields = ('nome',)
    list_filter = ('nome',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status')
    search_fields = ('usuario', 'status')
    list_filter = ('usuario', 'status')
    ordering = ('usuario', 'status')
    list_per_page = 10
    inlines = [ItensCompraInline]

@admin.register(ItemPedido)
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # Quantidade de itens adicionais
    

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pedido',)
    search_fields = ('pedido__id', )
    list_filter = ('pedido',)

@admin.register(MetodoDePagamento)
class MetodoDePagamentoAdmin(admin.ModelAdmin):
    list_display = ('cartao',)
    search_fields = ('cartao',)
    list_filter = ('cartao',)