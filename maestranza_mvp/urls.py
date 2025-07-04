from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventario.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/signup/',
         signup,
         name='signup'),

    
    path('accounts/login/',
         auth_views.LoginView.as_view(
             template_name='inventario/login.html'
         ),
         name='login'),

    
    path('accounts/logout/',
         auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),

    
    path('', include('inventario.urls', namespace='inventario')),
]
