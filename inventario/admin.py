from django.contrib import admin
from .models import (
    Proveedor, ElementoInventario, RecepcionCompra, 
    MovimientoInventario, SolicitudMaterial, AuditoriaInventario, Proyecto,
    Categoria, Etiqueta, ConfiguracionSistema
)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto')

@admin.register(ElementoInventario)
class ElementoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_serie', 'stock_actual', 'stock_minimo')
    search_fields = ('nombre', 'numero_serie', 'ubicacion')

@admin.register(RecepcionCompra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('elemento', 'cantidad', 'fecha')
    list_filter = ('fecha',)

@admin.register(MovimientoInventario)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('elemento', 'tipo', 'cantidad', 'usuario', 'fecha', 'proyecto')
    list_filter = ('tipo', 'fecha', 'usuario')
    search_fields = ('elemento__nombre', 'proyecto')

@admin.register(SolicitudMaterial)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'elemento', 'cantidad', 'proyecto', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('solicitante__username', 'elemento__nombre', 'proyecto')

@admin.register(AuditoriaInventario)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('auditor', 'elemento', 'stock_sistema', 'stock_fisico', 'diferencia', 'fecha_auditoria')
    list_filter = ('fecha_auditoria', 'auditor')
    search_fields = ('elemento__nombre', 'auditor__username')

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'gerente', 'estado', 'fecha_inicio', 'fecha_fin_estimada')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('nombre', 'gerente__username')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color')
    search_fields = ('nombre',)
    list_filter = ('color',)

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color')
    search_fields = ('nombre',)
    list_filter = ('color',)

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor', 'categoria', 'activo', 'fecha_modificacion', 'modificado_por')
    list_filter = ('categoria', 'activo', 'fecha_modificacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    ordering = ('categoria', 'nombre')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'valor', 'descripcion')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'activo')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_modificacion', 'modificado_por'),
            'classes': ('collapse',)
        }),
    )
