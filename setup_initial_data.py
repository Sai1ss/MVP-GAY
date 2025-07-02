#!/usr/bin/env python
"""
Script para configurar datos iniciales del sistema de inventario
Ejecutar con: python setup_initial_data.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maestranza_mvp.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from inventario.models import Proveedor, Categoria, Etiqueta, ElementoInventario

def create_groups():
    """Crear grupos de usuarios"""
    groups_data = [
        'Gestor de Inventario',
        'Comprador', 
        'Logística',
        'Auditor',
        'Jefe de Producción',
        'Gerente de Proyectos',
        'Usuario Final'
    ]
    
    for group_name in groups_data:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✅ Grupo '{group_name}' creado")
        else:
            print(f"ℹ️  Grupo '{group_name}' ya existe")

def create_users():
    """Crear usuarios de prueba"""
    users_data = [
        {
            'username': 'admin',
            'password': 'adminpass',
            'email': 'admin@maestranza.com',
            'is_superuser': True,
            'is_staff': True,
            'groups': []
        },
        {
            'username': 'gestor',
            'password': 'gestpass',
            'email': 'gestor@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Gestor de Inventario']
        },
        {
            'username': 'comprador',
            'password': 'comprpass',
            'email': 'comprador@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Comprador']
        },
        {
            'username': 'logistica',
            'password': 'logpass',
            'email': 'logistica@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Logística']
        },
        {
            'username': 'auditor',
            'password': 'audpass',
            'email': 'auditor@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Auditor']
        },
        {
            'username': 'produccion',
            'password': 'prodpass',
            'email': 'produccion@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Jefe de Producción']
        },
        {
            'username': 'gerente',
            'password': 'gerpass',
            'email': 'gerente@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Gerente de Proyectos']
        },
        {
            'username': 'usuario',
            'password': 'userpass',
            'email': 'usuario@maestranza.com',
            'is_superuser': False,
            'is_staff': False,
            'groups': ['Usuario Final']
        }
    ]
    
    for user_data in users_data:
        username = user_data['username']
        user, created = User.objects.get_or_create(username=username)
        
        if created:
            user.password = make_password(user_data['password'])
            user.email = user_data['email']
            user.is_superuser = user_data['is_superuser']
            user.is_staff = user_data['is_staff']
            user.save()
            
            # Asignar grupos
            for group_name in user_data['groups']:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            
            print(f"✅ Usuario '{username}' creado")
        else:
            print(f"ℹ️  Usuario '{username}' ya existe")

def create_proveedores():
    """Crear proveedores de prueba"""
    proveedores_data = [
        {'nombre': 'Metales Industriales S.A.', 'contacto': 'Juan Pérez - juan@metales.com'},
        {'nombre': 'Herramientas Pro Chile', 'contacto': 'María González - maria@herramientas.cl'},
        {'nombre': 'Suministros Maestranza Ltda.', 'contacto': 'Carlos Silva - carlos@suministros.cl'},
        {'nombre': 'Equipos Metalúrgicos', 'contacto': 'Ana Rodríguez - ana@equipos.cl'},
        {'nombre': 'Insumos Industriales del Sur', 'contacto': 'Roberto Vargas - roberto@insumos.cl'},
        {'nombre': 'Repuestos Mecánicos', 'contacto': 'Luis Méndez - luis@repuestos.cl'},
    ]
    
    for prov_data in proveedores_data:
        proveedor, created = Proveedor.objects.get_or_create(
            nombre=prov_data['nombre'],
            defaults={'contacto': prov_data['contacto']}
        )
        if created:
            print(f"✅ Proveedor '{prov_data['nombre']}' creado")
        else:
            print(f"ℹ️  Proveedor '{prov_data['nombre']}' ya existe")

def create_categorias():
    """Crear categorías de prueba"""
    categorias_data = [
        {'nombre': 'Herramientas Manuales', 'descripcion': 'Herramientas de uso manual para trabajos de maestranza', 'color': '#007bff'},
        {'nombre': 'Equipos Eléctricos', 'descripcion': 'Equipos y herramientas que funcionan con electricidad', 'color': '#28a745'},
        {'nombre': 'Materiales de Construcción', 'descripcion': 'Materiales básicos para construcción y reparación', 'color': '#ffc107'},
        {'nombre': 'Equipos de Seguridad', 'descripcion': 'Equipos y elementos de protección personal', 'color': '#dc3545'},
        {'nombre': 'Insumos de Soldadura', 'descripcion': 'Materiales y equipos para trabajos de soldadura', 'color': '#6f42c1'},
        {'nombre': 'Repuestos Mecánicos', 'descripcion': 'Repuestos para maquinaria y equipos', 'color': '#fd7e14'},
    ]
    
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={
                'descripcion': cat_data['descripcion'],
                'color': cat_data['color']
            }
        )
        if created:
            print(f"✅ Categoría '{cat_data['nombre']}' creada")
        else:
            print(f"ℹ️  Categoría '{cat_data['nombre']}' ya existe")

def create_etiquetas():
    """Crear etiquetas de prueba"""
    etiquetas_data = [
        {'nombre': 'Crítico', 'descripcion': 'Elementos críticos para operación', 'color': '#dc3545'},
        {'nombre': 'Alto Consumo', 'descripcion': 'Elementos de alto consumo', 'color': '#fd7e14'},
        {'nombre': 'Mantenimiento', 'descripcion': 'Para trabajos de mantenimiento', 'color': '#ffc107'},
        {'nombre': 'Producción', 'descripcion': 'Usado en línea de producción', 'color': '#28a745'},
        {'nombre': 'Emergencia', 'descripcion': 'Stock de emergencia', 'color': '#6f42c1'},
        {'nombre': 'Calidad', 'descripcion': 'Elementos de control de calidad', 'color': '#17a2b8'},
    ]
    
    for tag_data in etiquetas_data:
        etiqueta, created = Etiqueta.objects.get_or_create(
            nombre=tag_data['nombre'],
            defaults={
                'descripcion': tag_data['descripcion'],
                'color': tag_data['color']
            }
        )
        if created:
            print(f"✅ Etiqueta '{tag_data['nombre']}' creada")
        else:
            print(f"ℹ️  Etiqueta '{tag_data['nombre']}' ya existe")

def create_elementos_inventario():
    """Crear elementos de inventario de prueba"""
    elementos_data = [
        {
            'nombre': 'Taladro Industrial 1/2"',
            'descripcion': 'Taladro eléctrico industrial de 1/2 pulgada para trabajos pesados',
            'numero_serie': 'TAL-001-2024',
            'proveedor_nombre': 'Herramientas Pro Chile',
            'categoria_nombre': 'Equipos Eléctricos',
            'etiquetas': ['Alto Consumo', 'Producción'],
            'ubicacion': 'Almacén Principal - Estante A1',
            'stock_actual': 15,
            'stock_minimo': 5
        },
        {
            'nombre': 'Soldadora MIG 250A',
            'descripcion': 'Soldadora MIG industrial de 250 amperes',
            'numero_serie': 'SOL-002-2024',
            'proveedor_nombre': 'Equipos Metalúrgicos',
            'categoria_nombre': 'Insumos de Soldadura',
            'etiquetas': ['Crítico', 'Mantenimiento'],
            'ubicacion': 'Taller de Soldadura - Estante B2',
            'stock_actual': 3,
            'stock_minimo': 2
        },
        {
            'nombre': 'Casco de Seguridad',
            'descripcion': 'Casco de seguridad industrial certificado',
            'numero_serie': 'CAS-003-2024',
            'proveedor_nombre': 'Suministros Maestranza Ltda.',
            'categoria_nombre': 'Equipos de Seguridad',
            'etiquetas': ['Crítico', 'Emergencia'],
            'ubicacion': 'Almacén de EPP - Estante C1',
            'stock_actual': 50,
            'stock_minimo': 20
        },
        {
            'nombre': 'Llave Ajustable 12"',
            'descripcion': 'Llave ajustable de 12 pulgadas para trabajos generales',
            'numero_serie': 'LLA-004-2024',
            'proveedor_nombre': 'Metales Industriales S.A.',
            'categoria_nombre': 'Herramientas Manuales',
            'etiquetas': ['Alto Consumo', 'Mantenimiento'],
            'ubicacion': 'Caja de Herramientas - Estante A3',
            'stock_actual': 25,
            'stock_minimo': 10
        },
        {
            'nombre': 'Cable Eléctrico 2.5mm²',
            'descripcion': 'Cable eléctrico de 2.5mm² para instalaciones industriales',
            'numero_serie': 'CAB-005-2024',
            'proveedor_nombre': 'Insumos Industriales del Sur',
            'categoria_nombre': 'Materiales de Construcción',
            'etiquetas': ['Alto Consumo', 'Producción'],
            'ubicacion': 'Almacén de Materiales - Estante D2',
            'stock_actual': 200,
            'stock_minimo': 100
        },
        {
            'nombre': 'Rodamiento 6205',
            'descripcion': 'Rodamiento de bolas 6205 para maquinaria industrial',
            'numero_serie': 'ROD-006-2024',
            'proveedor_nombre': 'Repuestos Mecánicos',
            'categoria_nombre': 'Repuestos Mecánicos',
            'etiquetas': ['Crítico', 'Mantenimiento'],
            'ubicacion': 'Almacén de Repuestos - Estante E1',
            'stock_actual': 8,
            'stock_minimo': 5
        },
        {
            'nombre': 'Cinta Métrica 5m',
            'descripcion': 'Cinta métrica de 5 metros para mediciones precisas',
            'numero_serie': 'CIN-007-2024',
            'proveedor_nombre': 'Herramientas Pro Chile',
            'categoria_nombre': 'Herramientas Manuales',
            'etiquetas': ['Alto Consumo', 'Calidad'],
            'ubicacion': 'Caja de Herramientas - Estante A2',
            'stock_actual': 30,
            'stock_minimo': 15
        },
        {
            'nombre': 'Guantes de Cuero',
            'descripcion': 'Guantes de cuero para protección en trabajos manuales',
            'numero_serie': 'GUA-008-2024',
            'proveedor_nombre': 'Suministros Maestranza Ltda.',
            'categoria_nombre': 'Equipos de Seguridad',
            'etiquetas': ['Alto Consumo', 'Emergencia'],
            'ubicacion': 'Almacén de EPP - Estante C2',
            'stock_actual': 40,
            'stock_minimo': 25
        }
    ]
    
    for elem_data in elementos_data:
        # Verificar si ya existe
        if ElementoInventario.objects.filter(numero_serie=elem_data['numero_serie']).exists():
            print(f"ℹ️  Elemento '{elem_data['nombre']}' ya existe")
            continue
            
        try:
            # Obtener proveedor
            proveedor = Proveedor.objects.get(nombre=elem_data['proveedor_nombre'])
            
            # Obtener categoría
            categoria = Categoria.objects.get(nombre=elem_data['categoria_nombre'])
            
            # Crear elemento
            elemento = ElementoInventario.objects.create(
                nombre=elem_data['nombre'],
                descripcion=elem_data['descripcion'],
                numero_serie=elem_data['numero_serie'],
                proveedor=proveedor,
                categoria=categoria,
                ubicacion=elem_data['ubicacion'],
                stock_actual=elem_data['stock_actual'],
                stock_minimo=elem_data['stock_minimo']
            )
            
            # Agregar etiquetas
            for etiqueta_nombre in elem_data['etiquetas']:
                try:
                    etiqueta = Etiqueta.objects.get(nombre=etiqueta_nombre)
                    elemento.etiquetas.add(etiqueta)
                except Etiqueta.DoesNotExist:
                    print(f"⚠️  Etiqueta '{etiqueta_nombre}' no encontrada para '{elem_data['nombre']}'")
            
            print(f"✅ Elemento '{elem_data['nombre']}' creado")
            
        except Proveedor.DoesNotExist:
            print(f"⚠️  Proveedor '{elem_data['proveedor_nombre']}' no encontrado para '{elem_data['nombre']}'")
        except Categoria.DoesNotExist:
            print(f"⚠️  Categoría '{elem_data['categoria_nombre']}' no encontrada para '{elem_data['nombre']}'")

def main():
    print("🚀 Configurando datos iniciales del sistema...")
    print("=" * 60)
    
    create_groups()
    print("-" * 40)
    create_users()
    print("-" * 40)
    create_proveedores()
    print("-" * 40)
    create_categorias()
    print("-" * 40)
    create_etiquetas()
    print("-" * 40)
    create_elementos_inventario()
    print("-" * 40)
    
    print("✅ Configuración completada!")
    print("\n📋 Usuarios de prueba creados:")
    print("   - admin / adminpass (Superusuario)")
    print("   - gestor / gestpass (Gestor de Inventario)")
    print("   - comprador / comprpass (Comprador)")
    print("   - logistica / logpass (Logística)")
    print("   - auditor / audpass (Auditor)")
    print("   - produccion / prodpass (Jefe de Producción)")
    print("   - gerente / gerpass (Gerente de Proyectos)")
    print("   - usuario / userpass (Usuario Final)")
    print("\n🏭 Datos de prueba creados:")
    print("   - 5 Proveedores")
    print("   - 6 Categorías")
    print("   - 6 Etiquetas")
    print("   - 8 Elementos de inventario")
    print("\n🌐 Accede a http://127.0.0.1:8000/ para usar el sistema")

if __name__ == '__main__':
    main() 