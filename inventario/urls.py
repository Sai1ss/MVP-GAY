from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.index, name='index'),
    # Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    # Elementos
    path('elementos/nuevo/', views.elemento_create, name='elemento_create'),
    path('elementos/<int:pk>/editar/', views.elemento_update, name='elemento_update'),
    path('elementos/<int:pk>/borrar/', views.elemento_delete, name='elemento_delete'),
    # Recepciones
    path('recepciones/nueva/', views.recepcion_create, name='recepcion_create'),
]
