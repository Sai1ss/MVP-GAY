# inventario/decorators.py
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def role_required(role_name):
    """
    Permite el acceso si el usuario es superusuario o pertenece al grupo especificado.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and (
                user.is_superuser or
                user.groups.filter(name=role_name).exists()
            ):
                return view_func(request, *args, **kwargs)

            messages.error(request,
                "🚫 No tienes permiso para acceder a esta funcionalidad."
            )
            return redirect('inventario:index')
        return wrapper
    return decorator


def roles_required(*group_names):
    """
    Permite el acceso si el usuario es superusuario o pertenece a cualquiera de los grupos indicados.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and (
                user.is_superuser or
                user.groups.filter(name__in=group_names).exists()
            ):
                return view_func(request, *args, **kwargs)

            messages.error(request,
                "🚫 No tienes permiso para acceder a esta funcionalidad."
            )
            return redirect('inventario:index')
        return _wrapped
    return decorator
