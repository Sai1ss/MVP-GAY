# inventario/decorators.py
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def role_required(role_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.user
            # permiso para superusuario o miembro del grupo
            if user.is_authenticated and (
                user.is_superuser or
                user.groups.filter(name=role_name).exists()
            ):
                return view_func(request, *args, **kwargs)

            # si no tiene permiso, mostramos alerta y redirigimos
            messages.error(request,
                "🚫 No tienes permiso para acceder a esta funcionalidad."
            )
            return redirect('inventario:index')
        return wrapper
    return decorator
