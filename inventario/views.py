from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F, Q, Sum
from django.contrib.auth.models import User, Group   
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone
from .models import (
    Proveedor, ElementoInventario, RecepcionCompra, 
    MovimientoInventario, SolicitudMaterial, AuditoriaInventario, Proyecto,
    Categoria, Etiqueta, ConfiguracionSistema, AsignacionRecurso,
    crear_movimiento_automatico
)
from .forms import (
    ProveedorForm, ElementoForm, RecepcionForm, MovimientoInventarioForm,
    SolicitudMaterialForm, AuditoriaInventarioForm, ProyectoForm, SolicitudMaterialEditForm,
    ConfiguracionSistemaForm, UsuarioForm, AsignacionRecursoForm
)
from .decorators import role_required
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta


@login_required
@role_required('Gestor de Inventario')
def elemento_create(request):
    if request.method == 'POST':
        form = ElementoForm(request.POST)
        if form.is_valid():
            elemento = form.save()
            messages.success(
                request,
                f'Elemento "{elemento.nombre}" creado correctamente.'
            )
            return redirect('inventario:index')
    else:
        form = ElementoForm()

    return render(request, 'inventario/elemento_form.html', {
        'form': form,
        'is_edit': False,   # para el título
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect('inventario:index')

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect('inventario:index')

    
    return render(request, 'inventario/signup.html', {'form': form})


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('inventario:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('inventario:index')
        else:
            messages.error(request, 'Usuario o contraseña inválidos')

    return render(request, 'inventario/login.html')







def index(request):
    elementos = ElementoInventario.objects.all()
    
    # Búsqueda por texto
    query = request.GET.get('q')
    if query:
        elementos = elementos.filter(
            Q(nombre__icontains=query) |
            Q(numero_serie__icontains=query) |
            Q(lote__icontains=query) |
            Q(ubicacion__icontains=query)
        )
    
    # Filtros por categoría y etiqueta
    categoria_id = request.GET.get('categoria')
    etiqueta_id = request.GET.get('etiqueta')
    
    if categoria_id:
        elementos = elementos.filter(categoria_id=categoria_id)
    
    if etiqueta_id:
        elementos = elementos.filter(etiquetas__id=etiqueta_id)
    
    alertas = elementos.filter(stock_actual__lt=F('stock_minimo'))

    # Agregar información de precios para cada elemento
    for elemento in elementos:
        recepciones = RecepcionCompra.objects.filter(elemento=elemento).order_by('-fecha')
        if recepciones.exists():
            # Calcular precio promedio ponderado por cantidad
            total_costo = sum(r.precio_unitario * r.cantidad for r in recepciones)
            total_cantidad = sum(r.cantidad for r in recepciones)
            elemento.precio_promedio = total_costo / total_cantidad if total_cantidad > 0 else 0
            elemento.precio_ultimo = recepciones.first().precio_unitario
            elemento.total_recepciones = recepciones.count()
        else:
            elemento.precio_promedio = 0
            elemento.precio_ultimo = 0
            elemento.total_recepciones = 0

    is_gestor    = request.user.is_authenticated and request.user.groups.filter(name='Gestor de Inventario').exists()
    is_comprador = request.user.is_authenticated and request.user.groups.filter(name='Comprador').exists()
    is_admin     = request.user.is_authenticated and request.user.is_superuser

    usuarios = []   # lista vacía por defecto
    if is_admin:
        try:
            usuarios = User.objects.all().prefetch_related('groups')
        except Exception as e:
            # Log aquí si quieres: print("Error al traer usuarios:", e)
            usuarios = []

    # Obtener todas las categorías y etiquetas para los filtros
    categorias = Categoria.objects.all()
    etiquetas = Etiqueta.objects.all()

    # Fechas para alertas de vencimiento
    today = date.today()
    today_plus_30 = today + timedelta(days=30)
    today_plus_90 = today + timedelta(days=90)

    return render(request, 'inventario/index.html', {
        'elementos':    elementos,
        'alertas':      alertas,
        'is_gestor':    is_gestor,
        'is_comprador': is_comprador,
        'is_admin':     is_admin,
        'usuarios':     usuarios,
        'categorias':   categorias,
        'etiquetas':    etiquetas,
        'today_plus_30': today_plus_30,
        'today_plus_90': today_plus_90,
    })

# ---- Proveedores ----

@login_required
@role_required('Administrador del Sistema')
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'inventario/proveedor_list.html', {'proveedores': proveedores})

@login_required
@role_required('Administrador del Sistema')
def proveedor_create(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventario:proveedor_list')
    return render(request, 'inventario/proveedor_form.html', {'form': form})

@login_required
@role_required('Administrador del Sistema')
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado correctamente.')
        return redirect('inventario:proveedor_list')
    return render(request, 'inventario/proveedor_form.html', {'form': form, 'is_edit': True})

@login_required
@role_required('Administrador del Sistema')
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        if proveedor.elementoinventario_set.exists():
            messages.error(request, 'No se puede eliminar el proveedor porque tiene elementos asociados.')
            return redirect('inventario:proveedor_list')
        nombre = proveedor.nombre
        proveedor.delete()
        messages.success(request, f'Proveedor "{nombre}" eliminado correctamente.')
        return redirect('inventario:proveedor_list')
    return render(request, 'inventario/proveedor_confirm_delete.html', {'proveedor': proveedor})

# ---- Elementos ----

@login_required
@role_required('Gestor de Inventario')
def elemento_update(request, pk):
    elemento = get_object_or_404(ElementoInventario, pk=pk)
    form = ElementoForm(request.POST or None, instance=elemento)
    if form.is_valid():
        form.save()
        return redirect('inventario:index')
    return render(request, 'inventario/elemento_form.html', {'form': form})

@login_required
@role_required('Gestor de Inventario')
def elemento_delete(request, pk):
    elemento = get_object_or_404(ElementoInventario, pk=pk)
    if request.method == 'POST':
        elemento.delete()
        return redirect('inventario:index')
    return render(request, 'inventario/elemento_confirm_delete.html', {'elemento': elemento})

# ---- Recepción de Compras ----

@login_required
@role_required('Comprador')
def recepcion_create(request):
    form = RecepcionForm(request.POST or None)
    if form.is_valid():
        recepcion = form.save(commit=False)
        # Crear el movimiento automáticamente
        from .models import crear_movimiento_automatico
        recepcion.save()
        
        # Crear el movimiento automático
        crear_movimiento_automatico(
            elemento=recepcion.elemento,
            tipo='entrada',
            cantidad=recepcion.cantidad,
            usuario=request.user,
            origen='compra',
            observaciones=f'Compra - Precio: ${recepcion.precio_unitario}',
            recepcion_compra=recepcion
        )
        
        messages.success(request, f'Recepción de compra registrada: {recepcion.cantidad} unidades de {recepcion.elemento.nombre}')
        return redirect('inventario:index')
    return render(request, 'inventario/recepcion_form.html', {'form': form})

# ===== NUEVAS VISTAS PARA ROLES ESPECÍFICOS =====

# ---- Logística ----
@login_required
def movimiento_create(request):
    # Permitir acceso a Logística y Comprador
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Logística', 'Comprador']).exists()):
        messages.error(request, 'No tienes permisos para crear movimientos.')
        return redirect('inventario:index')
    form = MovimientoInventarioForm(request.POST or None)
    if form.is_valid():
        movimiento = form.save(commit=False)
        movimiento.usuario = request.user
        movimiento.origen = 'ajuste_manual'
        
        # Verificar stock para salidas
        if movimiento.tipo == 'salida' and movimiento.elemento.stock_actual < abs(movimiento.cantidad):
            messages.error(request, 'Stock insuficiente para esta salida.')
            return render(request, 'inventario/movimiento_form.html', {'form': form})
        
        # Crear movimiento usando la función automática
        from .models import crear_movimiento_automatico
        crear_movimiento_automatico(
            elemento=movimiento.elemento,
            tipo=movimiento.tipo,
            cantidad=movimiento.cantidad,
            usuario=request.user,
            origen='ajuste_manual',
            proyecto=movimiento.proyecto,
            observaciones=movimiento.observaciones
        )
        
        messages.success(request, f'Movimiento manual registrado: {movimiento.get_tipo_display()} de {abs(movimiento.cantidad)} unidades.')
        return redirect('inventario:movimiento_list')
    
    return render(request, 'inventario/movimiento_form.html', {'form': form})

@login_required
def movimiento_eliminar(request, pk):
    # Permitir acceso a Logística y Comprador
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Logística', 'Comprador']).exists()):
        messages.error(request, 'No tienes permisos para eliminar movimientos.')
        return redirect('inventario:movimiento_list')
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar movimientos.')
        return redirect('inventario:movimiento_list')
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '')
        if motivo:
            movimiento.eliminado = True
            movimiento.motivo_eliminacion = motivo
            movimiento.fecha_eliminacion = timezone.now()
            movimiento.usuario_eliminacion = request.user
            movimiento.save()
            messages.success(request, 'Movimiento eliminado correctamente.')
        else:
            messages.error(request, 'Debe especificar un motivo para la eliminación.')
        return redirect('inventario:movimiento_list')
    return render(request, 'inventario/movimiento_eliminar.html', {'movimiento': movimiento})

@login_required
def movimiento_restaurar(request, pk):
    # Permitir acceso a Logística y Comprador
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Logística', 'Comprador']).exists()):
        messages.error(request, 'No tienes permisos para restaurar movimientos.')
        return redirect('inventario:movimiento_list')
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para restaurar movimientos.')
        return redirect('inventario:movimiento_list')
    movimiento.eliminado = False
    movimiento.motivo_eliminacion = ''
    movimiento.fecha_eliminacion = None
    movimiento.usuario_eliminacion = None
    movimiento.save()
    messages.success(request, 'Movimiento restaurado correctamente.')
    return redirect('inventario:movimiento_list')

@login_required
def movimiento_list(request):
    # Permitir acceso a Logística y Comprador
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Logística', 'Comprador']).exists()):
        messages.error(request, 'No tienes permisos para acceder a los movimientos.')
        return redirect('inventario:index')
    mostrar_eliminados = request.GET.get('mostrar_eliminados', 'False') == 'True'
    if mostrar_eliminados and request.user.is_superuser:
        movimientos = MovimientoInventario.objects.select_related('elemento', 'usuario').order_by('-fecha')
    else:
        movimientos = MovimientoInventario.objects.filter(eliminado=False).select_related('elemento', 'usuario').order_by('-fecha')
    
    # Filtros
    elemento_id = request.GET.get('elemento')
    tipo = request.GET.get('tipo')
    origen = request.GET.get('origen')
    proyecto = request.GET.get('proyecto')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if elemento_id:
        movimientos = movimientos.filter(elemento_id=elemento_id)
    if tipo:
        movimientos = movimientos.filter(tipo=tipo)
    if origen:
        movimientos = movimientos.filter(origen=origen)
    if proyecto:
        movimientos = movimientos.filter(proyecto__icontains=proyecto)
    if fecha_desde:
        movimientos = movimientos.filter(fecha__date__gte=fecha_desde)
    if fecha_hasta:
        movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)
    
    # Obtener elementos para el filtro
    elementos = ElementoInventario.objects.all().order_by('nombre')
    
    # Estadísticas
    total_entradas = movimientos.filter(tipo='entrada').count()
    total_salidas = movimientos.filter(tipo='salida').count()
    total_ajustes = movimientos.filter(tipo='ajuste').count()
    
    context = {
        'movimientos': movimientos,
        'elementos': elementos,
        'total_entradas': total_entradas,
        'total_salidas': total_salidas,
        'total_ajustes': total_ajustes,
        'mostrar_eliminados': mostrar_eliminados,
        'es_admin': request.user.is_superuser,
        'filtros_activos': {
            'elemento_id': elemento_id,
            'tipo': tipo,
            'origen': origen,
            'proyecto': proyecto,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
        }
    }
    return render(request, 'inventario/movimiento_list.html', context)

# ---- Usuario Final ----
@login_required
@role_required('Usuario Final')
def solicitud_create(request):
    form = SolicitudMaterialForm(request.POST or None)
    if form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.solicitante = request.user
        solicitud.save()
        messages.success(request, 'Solicitud de material creada exitosamente.')
        return redirect('inventario:solicitud_list')
    
    return render(request, 'inventario/solicitud_form.html', {'form': form})

@login_required
def solicitud_list(request):
    # Permitir acceso a Usuario Final, Gestor de Inventario y superusuarios
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Usuario Final', 'Gestor de Inventario']).exists()):
        messages.error(request, 'No tienes permisos para acceder a las solicitudes.')
        return redirect('inventario:index')
    
    if request.user.groups.filter(name='Gestor de Inventario').exists() or request.user.is_superuser:
        solicitudes = SolicitudMaterial.objects.all().order_by('-fecha_solicitud')
        # Filtros para gestores
        estado = request.GET.get('estado')
        proyecto = request.GET.get('proyecto')
        if estado:
            solicitudes = solicitudes.filter(estado=estado)
        if proyecto:
            solicitudes = solicitudes.filter(proyecto__icontains=proyecto)
        is_gestor = True
    else:
        solicitudes = SolicitudMaterial.objects.filter(solicitante=request.user).order_by('-fecha_solicitud')
        is_gestor = False
    return render(request, 'inventario/solicitud_list.html', {'solicitudes': solicitudes, 'is_gestor': is_gestor})

@login_required
@role_required('Gestor de Inventario')
def solicitud_aprobar(request, pk):
    solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            messages.success(request, 'Solicitud aprobada.')
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            messages.warning(request, 'Solicitud rechazada.')
        elif accion == 'entregar':
            # Verificar stock disponible
            if solicitud.elemento.stock_actual >= solicitud.cantidad:
                solicitud.estado = 'entregada'
                solicitud.fecha_entrega = timezone.now()
                
                # Crear movimiento automático de salida
                from .models import crear_movimiento_automatico
                crear_movimiento_automatico(
                    elemento=solicitud.elemento,
                    tipo='salida',
                    cantidad=solicitud.cantidad,
                    usuario=request.user,
                    origen='solicitud',
                    proyecto=solicitud.proyecto,
                    observaciones=f'Solicitud #{solicitud.id} - {solicitud.solicitante.username}',
                    solicitud_material=solicitud
                )
                
                messages.success(request, f'Material entregado: {solicitud.cantidad} unidades de {solicitud.elemento.nombre}')
            else:
                messages.error(request, 'Stock insuficiente para entregar el material.')
                return redirect('inventario:solicitud_list')
        
        solicitud.save()
    
    return redirect('inventario:solicitud_list')

@login_required
@role_required('Gestor de Inventario')
def solicitud_update(request, pk):
    solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
    if request.method == 'POST':
        form = SolicitudMaterialEditForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud actualizada correctamente.')
            return redirect('inventario:solicitud_list')
    else:
        form = SolicitudMaterialEditForm(instance=solicitud)
    return render(request, 'inventario/solicitud_edit_form.html', {'form': form, 'solicitud': solicitud})

# ---- Auditor ----
@login_required
def auditoria_create(request):
    # Permitir acceso a Auditores y Gestores de Inventario
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Auditor', 'Gestor de Inventario']).exists()):
        messages.error(request, 'No tienes permisos para crear auditorías.')
        return redirect('inventario:index')
    form = AuditoriaInventarioForm(request.POST or None)
    if form.is_valid():
        auditoria = form.save(commit=False)
        auditoria.auditor = request.user
        auditoria.stock_sistema = auditoria.elemento.stock_actual
        auditoria.save()
        
        # Crear movimiento automático si hay diferencia
        if auditoria.diferencia != 0:
            from .models import crear_movimiento_automatico
            
            # Determinar tipo de ajuste
            if auditoria.diferencia > 0:
                tipo_ajuste = 'entrada'
                observacion = f'Ajuste por auditoría - Stock físico mayor al sistema (+{auditoria.diferencia})'
            else:
                tipo_ajuste = 'salida'
                observacion = f'Ajuste por auditoría - Stock físico menor al sistema ({auditoria.diferencia})'
            
            # Crear el movimiento automático
            crear_movimiento_automatico(
                elemento=auditoria.elemento,
                tipo=tipo_ajuste,
                cantidad=abs(auditoria.diferencia),
                usuario=request.user,
                origen='auditoria',
                observaciones=observacion,
                auditoria_inventario=auditoria
            )
            
            messages.warning(request, f'Auditoría completada. Stock ajustado automáticamente. Diferencia: {auditoria.diferencia:+d}')
        else:
            messages.success(request, 'Auditoría completada. Stock correcto.')
        
        return redirect('inventario:auditoria_list')
    
    return render(request, 'inventario/auditoria_form.html', {'form': form})

@login_required
def auditoria_list(request):
    # Permitir acceso a Auditores y Gestores de Inventario
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Auditor', 'Gestor de Inventario']).exists()):
        messages.error(request, 'No tienes permisos para acceder a las auditorías.')
        return redirect('inventario:index')
    
    auditorias = AuditoriaInventario.objects.select_related('elemento', 'auditor').order_by('-fecha_auditoria')
    return render(request, 'inventario/auditoria_list.html', {
        'auditorias': auditorias,
        'es_admin': request.user.is_superuser,
        'es_auditor': request.user.groups.filter(name='Auditor').exists(),
        'es_gestor': request.user.groups.filter(name='Gestor de Inventario').exists(),
    })

@login_required
def auditoria_edit(request, pk):
    # Permitir acceso a Auditores y Gestores de Inventario
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Auditor', 'Gestor de Inventario']).exists()):
        messages.error(request, 'No tienes permisos para editar auditorías.')
        return redirect('inventario:auditoria_list')
    
    auditoria = get_object_or_404(AuditoriaInventario, pk=pk)
    
    if request.method == 'POST':
        form = AuditoriaInventarioForm(request.POST, instance=auditoria)
        if form.is_valid():
            auditoria_editada = form.save(commit=False)
            # Recalcular diferencia
            auditoria_editada.diferencia = auditoria_editada.stock_fisico - auditoria_editada.stock_sistema
            auditoria_editada.save()
            
            # Si hay diferencia, crear movimiento de ajuste
            if auditoria_editada.diferencia != 0:
                from .models import crear_movimiento_automatico
                crear_movimiento_automatico(
                    elemento=auditoria_editada.elemento,
                    tipo='ajuste',
                    cantidad=auditoria_editada.diferencia,
                    usuario=request.user,
                    origen='auditoria',
                    observaciones=f'Ajuste por auditoría - Stock físico: {auditoria_editada.stock_fisico}, Sistema: {auditoria_editada.stock_sistema}',
                    auditoria_inventario=auditoria_editada
                )
                # Actualizar stock del elemento
                auditoria_editada.elemento.stock_actual = auditoria_editada.stock_fisico
                auditoria_editada.elemento.save()
                messages.warning(request, f'Auditoría actualizada. Stock ajustado. Diferencia: {auditoria_editada.diferencia}')
            else:
                messages.success(request, 'Auditoría actualizada. Stock correcto.')
            
            return redirect('inventario:auditoria_list')
    else:
        form = AuditoriaInventarioForm(instance=auditoria)
    
    return render(request, 'inventario/auditoria_form.html', {
        'form': form,
        'auditoria': auditoria,
        'titulo': 'Editar Auditoría'
    })

@login_required
def auditoria_eliminar(request, pk):
    # Permitir acceso a Auditores y Gestores de Inventario
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Auditor', 'Gestor de Inventario']).exists()):
        messages.error(request, 'No tienes permisos para eliminar auditorías.')
        return redirect('inventario:auditoria_list')
    
    auditoria = get_object_or_404(AuditoriaInventario, pk=pk)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '')
        if motivo:
            # Si la auditoría generó un movimiento de ajuste, revertirlo
            if auditoria.diferencia != 0:
                # Buscar el movimiento de ajuste generado por esta auditoría
                movimiento_ajuste = MovimientoInventario.objects.filter(
                    origen='auditoria',
                    auditoria_inventario=auditoria
                ).first()
                
                if movimiento_ajuste:
                    # Revertir el stock
                    auditoria.elemento.stock_actual -= auditoria.diferencia
                    auditoria.elemento.save()
                    # Eliminar el movimiento de ajuste
                    movimiento_ajuste.delete()
            
            auditoria.delete()
            messages.success(request, 'Auditoría eliminada correctamente.')
        else:
            messages.error(request, 'Debe proporcionar un motivo para eliminar la auditoría.')
            return render(request, 'inventario/auditoria_eliminar.html', {'auditoria': auditoria})
        
        return redirect('inventario:auditoria_list')
    
    return render(request, 'inventario/auditoria_eliminar.html', {'auditoria': auditoria})

# ---- Jefe de Producción ----
@login_required
@role_required('Jefe de Producción')
def proyecto_create(request):
    form = ProyectoForm(request.POST or None)
    if form.is_valid():
        proyecto = form.save(commit=False)
        proyecto.gerente = request.user
        proyecto.save()
        messages.success(request, f'Proyecto "{proyecto.nombre}" creado exitosamente.')
        return redirect('inventario:proyecto_list')
    
    return render(request, 'inventario/proyecto_form.html', {'form': form})

@login_required
@role_required('Jefe de Producción')
def proyecto_list(request):
    proyectos = Proyecto.objects.all()
    es_admin_o_gestor = request.user.is_superuser or request.user.groups.filter(name='Gestor de Inventario').exists()
    return render(request, 'inventario/proyecto_list.html', {
        'proyectos': proyectos,
        'es_admin_o_gestor': es_admin_o_gestor,
    })

@login_required
@role_required('Jefe de Producción')
def proyecto_detail(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    movimientos = MovimientoInventario.objects.filter(proyecto=proyecto.nombre).order_by('-fecha')
    return render(request, 'inventario/proyecto_detail.html', {
        'proyecto': proyecto,
        'movimientos': movimientos
    })

@login_required
@role_required('Jefe de Producción')
def proyecto_eliminar(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        nombre = proyecto.nombre
        proyecto.delete()
        messages.success(request, f'Proyecto "{nombre}" eliminado correctamente.')
        return redirect('inventario:proyecto_list')
    return render(request, 'inventario/proyecto_eliminar.html', {'proyecto': proyecto})

@login_required
@role_required('Jefe de Producción')
def proyecto_edit(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proyecto "{proyecto.nombre}" actualizado correctamente.')
            return redirect('inventario:proyecto_list')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'inventario/proyecto_form.html', {'form': form, 'is_edit': True, 'proyecto': proyecto})

# ---- Gerente de Proyectos ----
@login_required
@role_required('Gerente de Proyectos')
def dashboard_proyectos(request):
    proyectos = Proyecto.objects.all()
    total_proyectos = proyectos.count()
    proyectos_completados = proyectos.filter(estado='completado').count()
    proyectos_en_proceso = proyectos.filter(estado='en_proceso').count()
    proyectos_planificacion = proyectos.filter(estado='planificacion').count()
    
    return render(request, 'inventario/dashboard_proyectos.html', {
        'proyectos': proyectos,
        'total_proyectos': total_proyectos,
        'proyectos_completados': proyectos_completados,
        'proyectos_en_proceso': proyectos_en_proceso,
        'proyectos_planificacion': proyectos_planificacion
    })

# ---- Búsqueda para Logística y Comprador ----
@login_required
def buscar_elemento(request):
    # Permitir acceso a Logística y Comprador
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Logística', 'Comprador']).exists()):
        messages.error(request, 'No tienes permisos para buscar elementos.')
        return redirect('inventario:index')
    query = request.GET.get('q', '')
    elementos = []
    
    if query:
        elementos = ElementoInventario.objects.filter(
            Q(nombre__icontains=query) |
            Q(numero_serie__icontains=query) |
            Q(ubicacion__icontains=query)
        )
    
    return render(request, 'inventario/buscar_elemento.html', {
        'elementos': elementos,
        'query': query
    })

# ===== GESTIÓN DE CATEGORÍAS Y ETIQUETAS =====

# ---- Categorías ----
@login_required
@role_required('Gestor de Inventario')
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'inventario/categoria_list.html', {'categorias': categorias})

@login_required
@role_required('Gestor de Inventario')
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        color = request.POST.get('color', '#007bff')
        if nombre:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion, color=color)
            messages.success(request, f'Categoría "{nombre}" creada correctamente.')
            return redirect('inventario:categoria_list')
        else:
            messages.error(request, 'El nombre de la categoría es obligatorio.')
    return render(request, 'inventario/categoria_form.html')

@login_required
@role_required('Gestor de Inventario')
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        color = request.POST.get('color', '#007bff')
        if nombre:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            categoria.color = color
            categoria.save()
            messages.success(request, f'Categoría "{nombre}" actualizada correctamente.')
            return redirect('inventario:categoria_list')
        else:
            messages.error(request, 'El nombre de la categoría es obligatorio.')
    return render(request, 'inventario/categoria_form.html', {'categoria': categoria})

@login_required
@role_required('Gestor de Inventario')
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')
        return redirect('inventario:categoria_list')
    return render(request, 'inventario/categoria_confirm_delete.html', {'categoria': categoria})

# ---- Etiquetas ----
@login_required
@role_required('Gestor de Inventario')
def etiqueta_list(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'inventario/etiqueta_list.html', {'etiquetas': etiquetas})

@login_required
@role_required('Gestor de Inventario')
def etiqueta_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        color = request.POST.get('color', '#28a745')
        if nombre:
            Etiqueta.objects.create(nombre=nombre, descripcion=descripcion, color=color)
            messages.success(request, f'Etiqueta "{nombre}" creada correctamente.')
            return redirect('inventario:etiqueta_list')
        else:
            messages.error(request, 'El nombre de la etiqueta es obligatorio.')
    return render(request, 'inventario/etiqueta_form.html')

@login_required
@role_required('Gestor de Inventario')
def etiqueta_update(request, pk):
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        color = request.POST.get('color', '#28a745')
        if nombre:
            etiqueta.nombre = nombre
            etiqueta.descripcion = descripcion
            etiqueta.color = color
            etiqueta.save()
            messages.success(request, f'Etiqueta "{nombre}" actualizada correctamente.')
            return redirect('inventario:etiqueta_list')
        else:
            messages.error(request, 'El nombre de la etiqueta es obligatorio.')
    return render(request, 'inventario/etiqueta_form.html', {'etiqueta': etiqueta})

@login_required
@role_required('Gestor de Inventario')
def etiqueta_delete(request, pk):
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        nombre = etiqueta.nombre
        etiqueta.delete()
        messages.success(request, f'Etiqueta "{nombre}" eliminada correctamente.')
        return redirect('inventario:etiqueta_list')
    return render(request, 'inventario/etiqueta_confirm_delete.html', {'etiqueta': etiqueta})

def puede_ver_reportes(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__in=[
                'Gestor de Inventario',
                'Gerente de Proyectos',
                'Jefe de Producción'
            ]).exists()
        )
    )

@user_passes_test(puede_ver_reportes)
def reportes(request):
    # Filtros
    categoria_id = request.GET.get('categoria')
    proveedor_id = request.GET.get('proveedor')
    stock_bajo = request.GET.get('stock_bajo')
    vencidos = request.GET.get('vencidos')

    elementos = ElementoInventario.objects.all()
    if categoria_id:
        elementos = elementos.filter(categoria_id=categoria_id)
    if proveedor_id:
        elementos = elementos.filter(proveedor_id=proveedor_id)
    if stock_bajo == '1':
        elementos = elementos.filter(stock_actual__lt=F('stock_minimo'))
    if vencidos == '1':
        elementos = elementos.filter(fecha_vencimiento__isnull=False, fecha_vencimiento__lte=date.today())

    # Agregar información de precios para cada elemento
    for elemento in elementos:
        recepciones = RecepcionCompra.objects.filter(elemento=elemento).order_by('-fecha')
        if recepciones.exists():
            # Calcular precio promedio ponderado por cantidad
            total_costo = sum(r.precio_unitario * r.cantidad for r in recepciones)
            total_cantidad = sum(r.cantidad for r in recepciones)
            elemento.precio_promedio = total_costo / total_cantidad if total_cantidad > 0 else 0
            elemento.precio_ultimo = recepciones.first().precio_unitario
            elemento.total_recepciones = recepciones.count()
        else:
            elemento.precio_promedio = 0
            elemento.precio_ultimo = 0
            elemento.total_recepciones = 0

    # Análisis de piezas más utilizadas (para Jefe de Producción)
    movimientos_salida = MovimientoInventario.objects.filter(
        tipo__in=['salida', 'transferencia']
    ).values('elemento__nombre').annotate(
        total_consumo=Sum('cantidad')
    ).order_by('-total_consumo')[:10]

    # Análisis de consumo por proyecto
    consumo_por_proyecto = MovimientoInventario.objects.filter(
        tipo__in=['salida', 'transferencia'],
        proyecto__isnull=False
    ).exclude(proyecto='').values('proyecto').annotate(
        total_consumo=Sum('cantidad')
    ).order_by('-total_consumo')[:10]

    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    return render(request, 'inventario/reportes.html', {
        'elementos': elementos,
        'categorias': categorias,
        'proveedores': proveedores,
        'piezas_mas_utilizadas': movimientos_salida,
        'consumo_por_proyecto': consumo_por_proyecto,
        'filtros': {
            'categoria': categoria_id,
            'proveedor': proveedor_id,
            'stock_bajo': stock_bajo,
            'vencidos': vencidos,
        }
    })

# ===== HISTORIAL DE PRECIOS DE COMPRA =====

@login_required
@role_required('Comprador')
def historial_precios(request, elemento_id):
    elemento = get_object_or_404(ElementoInventario, pk=elemento_id)
    recepciones = RecepcionCompra.objects.filter(elemento=elemento).order_by('-fecha')
    
    # Calcular estadísticas
    if recepciones.exists():
        total_costo = sum(r.precio_unitario * r.cantidad for r in recepciones)
        total_cantidad = sum(r.cantidad for r in recepciones)
        precio_promedio = total_costo / total_cantidad if total_cantidad > 0 else 0
        precio_minimo = min(r.precio_unitario for r in recepciones)
        precio_maximo = max(r.precio_unitario for r in recepciones)
        precio_ultimo = recepciones.first().precio_unitario
    else:
        precio_promedio = precio_minimo = precio_maximo = precio_ultimo = 0
    
    return render(request, 'inventario/historial_precios.html', {
        'elemento': elemento,
        'recepciones': recepciones,
        'precio_promedio': precio_promedio,
        'precio_minimo': precio_minimo,
        'precio_maximo': precio_maximo,
        'precio_ultimo': precio_ultimo,
    })

# ===== NUEVA VISTA PARA HISTORIAL DE MOVIMIENTOS =====

@login_required
def historial_movimientos(request, elemento_id):
    """Vista para mostrar el historial completo de movimientos de un elemento"""
    elemento = get_object_or_404(ElementoInventario, pk=elemento_id)
    movimientos = MovimientoInventario.objects.filter(elemento=elemento).select_related('usuario').order_by('-fecha')
    
    # Filtros
    tipo = request.GET.get('tipo')
    origen = request.GET.get('origen')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if tipo:
        movimientos = movimientos.filter(tipo=tipo)
    if origen:
        movimientos = movimientos.filter(origen=origen)
    if fecha_desde:
        movimientos = movimientos.filter(fecha__date__gte=fecha_desde)
    if fecha_hasta:
        movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)
    
    # Estadísticas del elemento
    total_entradas = movimientos.filter(tipo='entrada').count()
    total_salidas = movimientos.filter(tipo='salida').count()
    total_ajustes = movimientos.filter(tipo='ajuste').count()
    
    # Calcular stock teórico basado en movimientos
    stock_teorico = 0
    for mov in movimientos.order_by('fecha'):
        if mov.tipo in ['entrada', 'devolucion']:
            stock_teorico += abs(mov.cantidad)
        elif mov.tipo in ['salida', 'transferencia']:
            stock_teorico -= abs(mov.cantidad)
        elif mov.tipo == 'ajuste':
            stock_teorico += mov.cantidad
    
    return render(request, 'inventario/historial_movimientos.html', {
        'elemento': elemento,
        'movimientos': movimientos,
        'total_entradas': total_entradas,
        'total_salidas': total_salidas,
        'total_ajustes': total_ajustes,
        'stock_actual': elemento.stock_actual,
        'stock_teorico': stock_teorico,
        'filtros_activos': {
            'tipo': tipo,
            'origen': origen,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
        }
    })

# ===== CONFIGURACIÓN DEL SISTEMA =====

@login_required
@role_required('Administrador del Sistema')
def configuracion_list(request):
    """Lista todas las configuraciones del sistema"""
    configuraciones = ConfiguracionSistema.objects.all().order_by('categoria', 'nombre')
    
    # Filtrar por categoría si se especifica
    categoria = request.GET.get('categoria')
    if categoria:
        configuraciones = configuraciones.filter(categoria=categoria)
    
    # Agrupar por categoría para mostrar en secciones
    configuraciones_por_categoria = {}
    for config in configuraciones:
        if config.categoria not in configuraciones_por_categoria:
            configuraciones_por_categoria[config.categoria] = []
        configuraciones_por_categoria[config.categoria].append(config)
    
    return render(request, 'inventario/configuracion_list.html', {
        'configuraciones_por_categoria': configuraciones_por_categoria,
        'categoria_actual': categoria
    })

@login_required
@role_required('Administrador del Sistema')
def configuracion_create(request):
    """Crear una nueva configuración del sistema"""
    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST)
        if form.is_valid():
            configuracion = form.save(commit=False)
            configuracion.modificado_por = request.user
            configuracion.save()
            messages.success(request, f'Configuración "{configuracion.nombre}" creada correctamente.')
            return redirect('inventario:configuracion_list')
    else:
        form = ConfiguracionSistemaForm()
    
    return render(request, 'inventario/configuracion_form.html', {
        'form': form,
        'titulo': 'Nueva Configuración'
    })

@login_required
@role_required('Administrador del Sistema')
def configuracion_update(request, pk):
    """Actualizar una configuración existente"""
    configuracion = get_object_or_404(ConfiguracionSistema, pk=pk)
    
    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST, instance=configuracion)
        if form.is_valid():
            configuracion = form.save(commit=False)
            configuracion.modificado_por = request.user
            configuracion.save()
            messages.success(request, f'Configuración "{configuracion.nombre}" actualizada correctamente.')
            return redirect('inventario:configuracion_list')
    else:
        form = ConfiguracionSistemaForm(instance=configuracion)
    
    return render(request, 'inventario/configuracion_form.html', {
        'form': form,
        'configuracion': configuracion,
        'titulo': 'Editar Configuración'
    })

@login_required
@role_required('Administrador del Sistema')
def configuracion_delete(request, pk):
    """Eliminar una configuración"""
    configuracion = get_object_or_404(ConfiguracionSistema, pk=pk)
    
    if request.method == 'POST':
        nombre = configuracion.nombre
        configuracion.delete()
        messages.success(request, f'Configuración "{nombre}" eliminada correctamente.')
        return redirect('inventario:configuracion_list')
    
    return render(request, 'inventario/configuracion_confirm_delete.html', {
        'configuracion': configuracion
    })

@login_required
@role_required('Administrador del Sistema')
def configuracion_toggle(request, pk):
    """Activar/desactivar una configuración"""
    configuracion = get_object_or_404(ConfiguracionSistema, pk=pk)
    configuracion.activo = not configuracion.activo
    configuracion.modificado_por = request.user
    configuracion.save()
    
    estado = "activada" if configuracion.activo else "desactivada"
    messages.success(request, f'Configuración "{configuracion.nombre}" {estado} correctamente.')
    return redirect('inventario:configuracion_list')

# ===== GESTIÓN DE USUARIOS =====

@login_required
@role_required('Administrador del Sistema')
def usuario_list(request):
    """Lista todos los usuarios del sistema"""
    usuarios = User.objects.all().order_by('username')
    
    # Filtrar por grupo si se especifica
    grupo = request.GET.get('grupo')
    if grupo:
        usuarios = usuarios.filter(groups__name=grupo)
    
    # Filtrar por estado (activo/inactivo)
    estado = request.GET.get('estado')
    if estado == 'activo':
        usuarios = usuarios.filter(is_active=True)
    elif estado == 'inactivo':
        usuarios = usuarios.filter(is_active=False)
    
    # Obtener grupos disponibles para filtros
    grupos = Group.objects.all().order_by('name')
    
    context = {
        'usuarios': usuarios,
        'grupos': grupos,
        'grupo_actual': grupo,
        'estado_actual': estado,
    }
    return render(request, 'inventario/usuario_list.html', context)

@login_required
@role_required('Administrador del Sistema')
def usuario_create(request):
    """Crear nuevo usuario"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Establecer contraseña temporal
            password = form.cleaned_data.get('password')
            if password:
                usuario.set_password(password)
            else:
                # Generar contraseña temporal
                import random
                import string
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                usuario.set_password(password)
            
            usuario.save()
            form.save_m2m()  # Guardar grupos
            
            messages.success(request, f'Usuario "{usuario.username}" creado exitosamente. Contraseña temporal: {password}')
            return redirect('inventario:usuario_list')
    else:
        form = UsuarioForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Usuario',
        'accion': 'Crear'
    }
    return render(request, 'inventario/usuario_form.html', context)

@login_required
@role_required('Administrador del Sistema')
def usuario_update(request, pk):
    """Editar usuario existente"""
    usuario = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            
            # Cambiar contraseña si se especifica
            password = form.cleaned_data.get('password')
            if password:
                usuario.set_password(password)
                messages.success(request, f'Contraseña de "{usuario.username}" actualizada exitosamente.')
            
            usuario.save()
            form.save_m2m()  # Guardar grupos
            
            messages.success(request, f'Usuario "{usuario.username}" actualizado exitosamente.')
            return redirect('inventario:usuario_list')
    else:
        form = UsuarioForm(instance=usuario)
    
    context = {
        'form': form,
        'usuario': usuario,
        'titulo': f'Editar Usuario: {usuario.username}',
        'accion': 'Actualizar'
    }
    return render(request, 'inventario/usuario_form.html', context)

@login_required
@role_required('Administrador del Sistema')
def usuario_toggle_active(request, pk):
    """Activar/desactivar usuario"""
    usuario = get_object_or_404(User, pk=pk)
    
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('inventario:usuario_list')
    
    usuario.is_active = not usuario.is_active
    usuario.save()
    
    estado = "activado" if usuario.is_active else "desactivado"
    messages.success(request, f'Usuario "{usuario.username}" {estado} exitosamente.')
    
    return redirect('inventario:usuario_list')

@login_required
@role_required('Administrador del Sistema')
def usuario_reset_password(request, pk):
    """Restablecer contraseña de usuario"""
    usuario = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        import random
        import string
        
        # Generar nueva contraseña temporal
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        usuario.set_password(new_password)
        usuario.save()
        
        messages.success(request, f'Nueva contraseña para "{usuario.username}": {new_password}')
        return redirect('inventario:usuario_list')
    
    context = {
        'usuario': usuario,
        'titulo': f'Restablecer Contraseña: {usuario.username}'
    }
    return render(request, 'inventario/usuario_reset_password.html', context)

@login_required
@role_required('Administrador del Sistema')
def usuario_delete(request, pk):
    """Eliminar usuario"""
    usuario = get_object_or_404(User, pk=pk)
    
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('inventario:usuario_list')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{username}" eliminado exitosamente.')
        return redirect('inventario:usuario_list')
    
    context = {
        'usuario': usuario,
        'titulo': f'Eliminar Usuario: {usuario.username}'
    }
    return render(request, 'inventario/usuario_confirm_delete.html', context)

# ---- Asignaciones de Recursos ----

@login_required
@role_required('Jefe de Producción')
def asignacion_create(request):
    form = AsignacionRecursoForm(request.POST or None)
    if form.is_valid():
        try:
            asignacion = form.save(usuario=request.user)
            asignacion.cantidad_disponible = asignacion.cantidad_asignada
            asignacion.save()
            
            # Crear movimiento automático de reserva
            crear_movimiento_automatico(
                elemento=asignacion.elemento,
                tipo='salida',
                cantidad=asignacion.cantidad_asignada,
                usuario=request.user,
                proyecto=asignacion.proyecto,
                observaciones=f'Reserva para proyecto: {asignacion.proyecto}'
            )
            
            messages.success(request, f'Recurso asignado correctamente al proyecto "{asignacion.proyecto}".')
            return redirect('inventario:asignacion_list')
        except ValueError as e:
            messages.error(request, str(e))
    
    return render(request, 'inventario/asignacion_form.html', {
        'form': form,
        'is_edit': False
    })

@login_required
@role_required('Jefe de Producción')
def asignacion_list(request):
    asignaciones = AsignacionRecurso.objects.all().select_related('elemento', 'asignado_por')
    
    # Filtros
    estado = request.GET.get('estado')
    proyecto = request.GET.get('proyecto')
    elemento_id = request.GET.get('elemento')
    
    if estado:
        asignaciones = asignaciones.filter(estado=estado)
    if proyecto:
        asignaciones = asignaciones.filter(proyecto__icontains=proyecto)
    if elemento_id:
        asignaciones = asignaciones.filter(elemento_id=elemento_id)
    
    # Estadísticas
    total_asignado = sum(a.cantidad_asignada for a in asignaciones.filter(estado__in=['reservado', 'en_uso']))
    total_disponible = sum(a.cantidad_disponible for a in asignaciones.filter(estado__in=['reservado', 'en_uso']))
    
    elementos = ElementoInventario.objects.all()
    
    return render(request, 'inventario/asignacion_list.html', {
        'asignaciones': asignaciones,
        'elementos': elementos,
        'estadisticas': {
            'total_asignado': total_asignado,
            'total_disponible': total_disponible,
            'total_uso': total_asignado - total_disponible
        },
        'filtros': {
            'estado': estado,
            'proyecto': proyecto,
            'elemento': elemento_id
        }
    })

@login_required
@role_required('Jefe de Producción')
def asignacion_detail(request, pk):
    asignacion = get_object_or_404(AsignacionRecurso, pk=pk)
    return render(request, 'inventario/asignacion_detail.html', {
        'asignacion': asignacion
    })

@login_required
@role_required('Jefe de Producción')
def asignacion_edit(request, pk):
    asignacion = get_object_or_404(AsignacionRecurso, pk=pk)
    
    if asignacion.estado in ['liberado', 'cancelado']:
        messages.error(request, 'No se puede editar una asignación liberada o cancelada.')
        return redirect('inventario:asignacion_list')
    
    form = AsignacionRecursoForm(request.POST or None, instance=asignacion)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Asignación actualizada correctamente.')
            return redirect('inventario:asignacion_list')
        except ValueError as e:
            messages.error(request, str(e))
    
    return render(request, 'inventario/asignacion_form.html', {
        'form': form,
        'is_edit': True,
        'asignacion': asignacion
    })

@login_required
@role_required('Jefe de Producción')
def asignacion_liberar(request, pk):
    asignacion = get_object_or_404(AsignacionRecurso, pk=pk)
    
    if request.method == 'POST':
        try:
            asignacion.liberar(request.user)
            messages.success(request, f'Asignación liberada correctamente. {asignacion.cantidad_disponible} unidades devueltas.')
            return redirect('inventario:asignacion_list')
        except Exception as e:
            messages.error(request, f'Error al liberar la asignación: {str(e)}')
    
    return render(request, 'inventario/asignacion_confirm_liberar.html', {
        'asignacion': asignacion
    })

@login_required
@role_required('Jefe de Producción')
def asignacion_cancelar(request, pk):
    asignacion = get_object_or_404(AsignacionRecurso, pk=pk)
    
    if request.method == 'POST':
        try:
            asignacion.cancelar(request.user)
            messages.success(request, f'Asignación cancelada correctamente. {asignacion.cantidad_disponible} unidades devueltas.')
            return redirect('inventario:asignacion_list')
        except Exception as e:
            messages.error(request, f'Error al cancelar la asignación: {str(e)}')
    
    return render(request, 'inventario/asignacion_confirm_cancelar.html', {
        'asignacion': asignacion
    })

@login_required
@role_required('Jefe de Producción')
def asignacion_consumir(request, pk):
    asignacion = get_object_or_404(AsignacionRecurso, pk=pk)
    
    if request.method == 'POST':
        cantidad_consumir = int(request.POST.get('cantidad_consumir', 0))
        
        if cantidad_consumir <= 0:
            messages.error(request, 'La cantidad debe ser mayor a 0.')
        elif cantidad_consumir > asignacion.cantidad_disponible:
            messages.error(request, f'No hay suficiente cantidad disponible. Disponible: {asignacion.cantidad_disponible}')
        else:
            try:
                # Actualizar cantidad disponible
                asignacion.cantidad_disponible -= cantidad_consumir
                if asignacion.cantidad_disponible == 0:
                    asignacion.estado = 'en_uso'
                asignacion.save()
                
                # Crear movimiento de consumo
                crear_movimiento_automatico(
                    elemento=asignacion.elemento,
                    tipo='salida',
                    cantidad=cantidad_consumir,
                    usuario=request.user,
                    proyecto=asignacion.proyecto,
                    observaciones=f'Consumo de asignación - {cantidad_consumir} unidades utilizadas'
                )
                
                messages.success(request, f'{cantidad_consumir} unidades consumidas correctamente.')
                return redirect('inventario:asignacion_detail', pk=pk)
            except Exception as e:
                messages.error(request, f'Error al consumir recursos: {str(e)}')
    
    return render(request, 'inventario/asignacion_consumir.html', {
        'asignacion': asignacion
    })
