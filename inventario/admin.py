from django.contrib import admin
from .models import Proveedor, ElementoInventario, RecepcionCompra

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto')

@admin.register(ElementoInventario)
class ElementoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_serie', 'stock_actual', 'stock_minimo')

@admin.register(RecepcionCompra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('elemento', 'cantidad', 'fecha')
