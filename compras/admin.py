from django.contrib import admin
from .models import ItemCompra, ListaCompraMensal


class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 1


@admin.register(ListaCompraMensal)
class ListaCompraMensalAdmin(admin.ModelAdmin):
    list_display = ('mes', 'ano', 'criado_em', 'total_itens', 'total_comprados', 'total_pendentes')
    list_filter = ('ano', 'mes')
    inlines = [ItemCompraInline]


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'lista', 'quantidade', 'comprado', 'criado_em')
    list_filter = ('comprado', 'lista__ano', 'lista__mes')
    search_fields = ('nome', 'quantidade', 'observacao')
