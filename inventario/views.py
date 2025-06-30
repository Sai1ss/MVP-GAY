from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.auth.models import User   
from .models import Proveedor, ElementoInventario, RecepcionCompra
from .forms import ProveedorForm, ElementoForm, RecepcionForm
from .decorators import role_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


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
    alertas   = elementos.filter(stock_actual__lt=F('stock_minimo'))

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

    return render(request, 'inventario/index.html', {
        'elementos':    elementos,
        'alertas':      alertas,
        'is_gestor':    is_gestor,
        'is_comprador': is_comprador,
        'is_admin':     is_admin,
        'usuarios':     usuarios,
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

# ---- Elementos ----

@login_required
@role_required('Gestor de Inventario')
def elemento_create(request):
    form = ElementoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventario:index')
    return render(request, 'inventario/elemento_form.html', {'form': form})

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
        form.save()
        return redirect('inventario:index')
    return render(request, 'inventario/recepcion_form.html', {'form': form})
