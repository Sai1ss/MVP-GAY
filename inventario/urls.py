from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),
    
    # Elementos
    path('elementos/nuevo/', views.elemento_create, name='elemento_create'),
    path('elementos/<int:pk>/editar/', views.elemento_update, name='elemento_update'),
    path('elementos/<int:pk>/borrar/', views.elemento_delete, name='elemento_delete'),
    
    # Recepciones
    path('recepciones/nueva/', views.recepcion_create, name='recepcion_create'),
    
    # Logística
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/eliminar/<int:pk>/', views.movimiento_eliminar, name='movimiento_eliminar'),
    path('movimientos/restaurar/<int:pk>/', views.movimiento_restaurar, name='movimiento_restaurar'),
    path('buscar/', views.buscar_elemento, name='buscar_elemento'),
    
    # Usuario Final
    path('solicitudes/', views.solicitud_list, name='solicitud_list'),
    path('solicitudes/nueva/', views.solicitud_create, name='solicitud_create'),
    path('solicitudes/<int:pk>/aprobar/', views.solicitud_aprobar, name='solicitud_aprobar'),
    path('solicitudes/<int:pk>/editar/', views.solicitud_update, name='solicitud_update'),
    
    # Auditorías
    path('auditorias/', views.auditoria_list, name='auditoria_list'),
    path('auditorias/nueva/', views.auditoria_create, name='auditoria_create'),
    path('auditorias/editar/<int:pk>/', views.auditoria_edit, name='auditoria_edit'),
    path('auditorias/eliminar/<int:pk>/', views.auditoria_eliminar, name='auditoria_eliminar'),
    
    # Jefe de Producción
    path('proyectos/', views.proyecto_list, name='proyecto_list'),
    path('proyectos/nuevo/', views.proyecto_create, name='proyecto_create'),
    path('proyectos/<int:pk>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyectos/eliminar/<int:pk>/', views.proyecto_eliminar, name='proyecto_eliminar'),
    path('proyectos/editar/<int:pk>/', views.proyecto_edit, name='proyecto_edit'),
    
    # Gerente de Proyectos
    path('dashboard-proyectos/', views.dashboard_proyectos, name='dashboard_proyectos'),
    
    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    
    # Etiquetas
    path('etiquetas/', views.etiqueta_list, name='etiqueta_list'),
    path('etiquetas/nueva/', views.etiqueta_create, name='etiqueta_create'),
    path('etiquetas/<int:pk>/editar/', views.etiqueta_update, name='etiqueta_update'),
    path('etiquetas/<int:pk>/eliminar/', views.etiqueta_delete, name='etiqueta_delete'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    
    # Historial de Precios
    path('elementos/<int:elemento_id>/historial-precios/', views.historial_precios, name='historial_precios'),
    
    # Historial de Movimientos
    path('elementos/<int:elemento_id>/historial-movimientos/', views.historial_movimientos, name='historial_movimientos'),
    
    # Configuración del Sistema
    path('configuracion/', views.configuracion_list, name='configuracion_list'),
    path('configuracion/nueva/', views.configuracion_create, name='configuracion_create'),
    path('configuracion/<int:pk>/editar/', views.configuracion_update, name='configuracion_update'),
    path('configuracion/<int:pk>/eliminar/', views.configuracion_delete, name='configuracion_delete'),
    path('configuracion/<int:pk>/toggle/', views.configuracion_toggle, name='configuracion_toggle'),
    
    # Gestión de Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/toggle/', views.usuario_toggle_active, name='usuario_toggle_active'),
    path('usuarios/<int:pk>/reset-password/', views.usuario_reset_password, name='usuario_reset_password'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),
    
    # Asignaciones de Recursos
    path('asignaciones/', views.asignacion_list, name='asignacion_list'),
    path('asignaciones/nueva/', views.asignacion_create, name='asignacion_create'),
    path('asignaciones/<int:pk>/', views.asignacion_detail, name='asignacion_detail'),
    path('asignaciones/<int:pk>/editar/', views.asignacion_edit, name='asignacion_edit'),
    path('asignaciones/<int:pk>/liberar/', views.asignacion_liberar, name='asignacion_liberar'),
    path('asignaciones/<int:pk>/cancelar/', views.asignacion_cancelar, name='asignacion_cancelar'),
    path('asignaciones/<int:pk>/consumir/', views.asignacion_consumir, name='asignacion_consumir'),

    #compras
    path('ordenes-compra/',             views.orden_compra_list,   name='orden_compra_list'),
    path('ordenes-compra/nueva/',       views.orden_compra_create, name='orden_compra_create'),
    path('ordenes-compra/<int:pk>/',    views.orden_compra_detail, name='orden_compra_detail'),
    path('ordenes-compra/<int:pk>/recibir/', views.orden_compra_receive, name='orden_compra_receive'),

]
