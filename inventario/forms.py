from django import forms
from .models import Proveedor, ElementoInventario, RecepcionCompra

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control'}),
        }

class ElementoForm(forms.ModelForm):
    class Meta:
        model = ElementoInventario
        fields = [
            'nombre','descripcion','numero_serie',
            'proveedor','ubicacion','stock_actual','stock_minimo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'numero_serie': forms.TextInput(attrs={'class':'form-control'}),
            'proveedor': forms.Select(attrs={'class':'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class':'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class':'form-control'}),
        }

class RecepcionForm(forms.ModelForm):
    class Meta:
        model = RecepcionCompra
        fields = ['elemento','cantidad']
        widgets = {
            'elemento': forms.Select(attrs={'class':'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control','min':1}),
        }
    def clean_cantidad(self):
        c = self.cleaned_data['cantidad']
        if c <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return c
