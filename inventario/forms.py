from django import forms
from .models import Proveedor, ElementoInventario, RecepcionCompra, MovimientoInventario, SolicitudMaterial, AuditoriaInventario, Proyecto, Categoria, Etiqueta, ConfiguracionSistema, AsignacionRecurso
from django.contrib.auth.models import User

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control'}),
        }

class ElementoForm(forms.ModelForm):
    # Campos adicionales para información de precios (solo informativos)
    precio_estimado = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control', 'min':'0.01', 'step':'0.01'})
    )
    
    class Meta:
        model = ElementoInventario
        fields = [
            'nombre','descripcion','numero_serie',
            'proveedor','categoria','etiquetas','ubicacion',
            'lote','fecha_vencimiento',
            'stock_actual','stock_minimo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'numero_serie': forms.TextInput(attrs={'class':'form-control'}),
            'proveedor': forms.Select(attrs={'class':'form-select'}),
            'categoria': forms.Select(attrs={'class':'form-select'}),
            'etiquetas': forms.SelectMultiple(attrs={'class':'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control'}),
            'lote': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'stock_actual': forms.NumberInput(attrs={'class':'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class':'form-control'}),
        }

class RecepcionForm(forms.ModelForm):
    class Meta:
        model = RecepcionCompra
        fields = ['elemento','cantidad','precio_unitario']
        widgets = {
            'elemento': forms.Select(attrs={'class':'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control','min':1}),
            'precio_unitario': forms.NumberInput(attrs={'class':'form-control','min':'0.01','step':'0.01'}),
        }
    def clean_cantidad(self):
        c = self.cleaned_data['cantidad']
        if c <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return c
    
    def clean_precio_unitario(self):
        precio = self.cleaned_data['precio_unitario']
        if precio <= 0:
            raise forms.ValidationError("El precio unitario debe ser mayor que cero.")
        return precio

# Nuevos formularios para funcionalidades específicas de roles

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['elemento', 'tipo', 'cantidad', 'proyecto', 'observaciones']
        widgets = {
            'elemento': forms.Select(attrs={'class':'form-select'}),
            'tipo': forms.Select(attrs={'class':'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control'}),
            'proyecto': forms.TextInput(attrs={'class':'form-control'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class SolicitudMaterialForm(forms.ModelForm):
    class Meta:
        model = SolicitudMaterial
        fields = ['elemento', 'cantidad', 'proyecto', 'observaciones']
        widgets = {
            'elemento': forms.Select(attrs={'class':'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control', 'min':1}),
            'proyecto': forms.TextInput(attrs={'class':'form-control'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class SolicitudMaterialEditForm(forms.ModelForm):
    class Meta:
        model = SolicitudMaterial
        fields = ['estado', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class':'form-select'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class AuditoriaInventarioForm(forms.ModelForm):
    class Meta:
        model = AuditoriaInventario
        fields = ['elemento', 'stock_fisico', 'observaciones']
        widgets = {
            'elemento': forms.Select(attrs={'class':'form-select'}),
            'stock_fisico': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
            'observaciones': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin_estimada', 'presupuesto', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'fecha_inicio': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'fecha_fin_estimada': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'presupuesto': forms.NumberInput(attrs={'class':'form-control', 'step':'0.01'}),
            'estado': forms.Select(attrs={'class':'form-select'}),
        }

class ConfiguracionSistemaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSistema
        fields = ['nombre', 'valor', 'descripcion', 'categoria', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'valor': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'categoria': forms.Select(attrs={'class':'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre:
            raise forms.ValidationError("El nombre de la configuración es obligatorio.")
        return nombre
    
    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if not valor:
            raise forms.ValidationError("El valor de la configuración es obligatorio.")
        return valor

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Deja vacío para mantener la contraseña actual o generar una temporal'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'is_active', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        
        # Verificar si el username ya existe (excepto para el usuario actual)
        if self.instance.pk:
            if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
                raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            # Verificar si el email ya existe (excepto para el usuario actual)
            if self.instance.pk:
                if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                    raise forms.ValidationError("Este email ya está en uso.")
            else:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError("Este email ya está en uso.")
        
        return email

class AsignacionRecursoForm(forms.ModelForm):
    class Meta:
        model = AsignacionRecurso
        fields = ['elemento', 'proyecto', 'cantidad_asignada', 'fecha_liberacion_estimada', 'observaciones']
        widgets = {
            'elemento': forms.Select(attrs={'class': 'form-select'}),
            'proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto'}),
            'cantidad_asignada': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'fecha_liberacion_estimada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo elementos con stock disponible
        self.fields['elemento'].queryset = ElementoInventario.objects.filter(stock_actual__gt=0)
    
    def clean(self):
        cleaned_data = super().clean()
        elemento = cleaned_data.get('elemento')
        cantidad_asignada = cleaned_data.get('cantidad_asignada')
        
        if elemento and cantidad_asignada:
            # Verificar stock disponible considerando otras asignaciones activas
            stock_disponible = elemento.stock_actual
            asignaciones_activas = AsignacionRecurso.objects.filter(
                elemento=elemento,
                estado__in=['reservado', 'en_uso']
            )
            
            if self.instance.pk:
                asignaciones_activas = asignaciones_activas.exclude(pk=self.instance.pk)
            
            stock_reservado = sum(a.cantidad_asignada for a in asignaciones_activas)
            stock_realmente_disponible = stock_disponible - stock_reservado
            
            if cantidad_asignada > stock_realmente_disponible:
                raise forms.ValidationError(
                    f"No hay suficiente stock disponible. "
                    f"Stock total: {stock_disponible}, "
                    f"Reservado: {stock_reservado}, "
                    f"Disponible: {stock_realmente_disponible}"
                )
        
        return cleaned_data
    
    def save(self, commit=True, usuario=None):
        asignacion = super().save(commit=False)
        if usuario:
            asignacion.asignado_por = usuario
        # Establecer cantidad_disponible igual a cantidad_asignada al crear
        if not asignacion.pk:  # Si es una nueva asignación
            asignacion.cantidad_disponible = asignacion.cantidad_asignada
        if commit:
            asignacion.save()
        return asignacion
