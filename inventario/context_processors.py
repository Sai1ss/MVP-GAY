# inventario/context_processors.py
def role_flags(request):
    user = request.user
    return {
        'is_admin':    user.is_authenticated and user.is_superuser,
        'is_gestor':   user.is_authenticated and user.groups.filter(name='Gestor de Inventario').exists(),
        'is_comprador':user.is_authenticated and user.groups.filter(name='Comprador').exists(),
        
    }
