# inventario/context_processors.py
def role_flags(request):
    user = request.user
    return {
        'is_admin':    user.is_authenticated and user.is_superuser,
        'is_gestor':   user.is_authenticated and user.groups.filter(name='Gestor de Inventario').exists(),
        'is_comprador':user.is_authenticated and user.groups.filter(name='Comprador').exists(),
        'is_logistica':user.is_authenticated and user.groups.filter(name='Logística').exists(),
        'is_auditor':  user.is_authenticated and user.groups.filter(name='Auditor').exists(),
        'is_produccion':user.is_authenticated and user.groups.filter(name='Jefe de Producción').exists(),
        'is_gerente_proyecto':user.is_authenticated and user.groups.filter(name='Gerente de Proyectos').exists(),
        'is_usuario_final':user.is_authenticated and user.groups.filter(name='Usuario Final').exists(),
    }
