# MVP Control de Inventarios - Maestranzas Unidos S.A.

Sistema web de gestión de inventario desarrollado en Django para empresas maestranza.

## 🚀 Instalación y Configuración

### 1. Preparar el entorno
```bash
# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar la base de datos
```bash
# Aplicar migraciones
python manage.py migrate

# Crear usuarios y grupos iniciales
python setup_initial_data.py
```

### 3. Ejecutar el servidor
```bash
python manage.py runserver
```

### 4. Acceder al sistema
- **URL principal:** http://127.0.0.1:8000/
- **Admin Django:** http://127.0.0.1:8000/admin/

## 👥 Usuarios de Prueba

| Perfil                  | Usuario     | Contraseña   |
|-------------------------|-------------|--------------|
| Superusuario            | admin       | adminpass    |
| Gestor de Inventario    | gestor      | gestpass     |
| Comprador               | comprador   | comprpass    |
| Logística               | logistica   | logpass      |
| Auditor                 | auditor     | audpass      |
| Jefe de Producción      | produccion  | prodpass     |
| Gerente de Proyectos    | gerente     | gerpass      |
| Usuario Final           | usuario     | userpass     |

Puedes usar cualquiera de estas cuentas para probar el sistema según el perfil correspondiente.

## 🛠️ Funcionalidades

### ✅ Implementadas
- **Autenticación y roles** con permisos específicos
- **CRUD completo** de inventario, proveedores y recepciones
- **Alertas de stock bajo** automáticas
- **Interfaz responsive** con Bootstrap 5
- **Sistema de roles** granular
- **Historial de compras** con actualización automática de stock
- **Gestión de categorías y etiquetas** con colores personalizables
- **Control de lotes y fechas de vencimiento** con alertas visuales
- **Módulo de reportes** con filtros avanzados
- **Historial de precios de compra** con estadísticas y análisis

### 🔧 Roles del Sistema
- **Administrador:** Acceso total al sistema
- **Gestor de Inventario:** Gestionar elementos del inventario
- **Comprador:** Registrar recepciones de compra
- **Logística:** (Preparado para futuras funcionalidades)
- **Auditor:** (Preparado para futuras funcionalidades)

## 📁 Estructura del Proyecto

```
MVP-GAY/
├── maestranza_mvp/          # Configuración principal de Django
├── inventario/              # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Lógica de negocio
│   ├── forms.py            # Formularios
│   ├── templates/          # Plantillas HTML
│   └── static/             # Archivos estáticos (CSS/JS)
├── db.sqlite3              # Base de datos SQLite
├── requirements.txt        # Dependencias de Python
└── setup_initial_data.py   # Script de configuración inicial
```

## 🎨 Tecnologías Utilizadas

- **Backend:** Django 4.2+
- **Base de datos:** SQLite3
- **Frontend:** Bootstrap 5.3.2 + CSS personalizado
- **Iconos:** Font Awesome 6.4.0
- **Formularios:** django-widget-tweaks

## 🔒 Seguridad

- Autenticación basada en sesiones
- Control de acceso por roles
- Protección CSRF habilitada
- Validación de formularios

## 📝 Notas de Desarrollo

- **Modo DEBUG:** Habilitado para desarrollo
- **SECRET_KEY:** Cambiar en producción
- **Base de datos:** SQLite para desarrollo, migrar a PostgreSQL en producción

## 🐛 Solución de Problemas

### Error: "pip no se reconoce"
```bash
# Usar python -m pip en lugar de pip
python -m pip install -r requirements.txt
```

### Error: "No module named 'widget_tweaks'"
```bash
# Instalar manualmente
pip install django-widget-tweaks
```

### Error: "Database is locked"
- Cerrar el servidor Django
- Verificar que no hay otros procesos usando la base de datos
- Reiniciar el servidor

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contactar al equipo de desarrollo.

## Funcionalidades por perfil de usuario

| Perfil                  | Funcionalidades principales |
|-------------------------|----------------------------|
| Superusuario            | Acceso total, gestión de usuarios y proveedores, administración completa del sistema |
| Gestor de Inventario    | CRUD de inventario, categorías y etiquetas, aprobación de solicitudes, gestión de stock, reportes |
| Comprador               | Registrar recepciones de compra, ver historial de precios de compra |
| Logística               | Registrar movimientos de inventario (entradas/salidas), búsqueda de elementos |
| Auditor                 | Realizar auditorías de inventario, ver diferencias de stock |
| Jefe de Producción      | Crear y gestionar proyectos, ver detalles de proyectos |
| Gerente de Proyectos    | Dashboard de proyectos, visión general de todos los proyectos, reportes |
| Usuario Final           | Crear solicitudes de materiales, ver estado de sus solicitudes |

> Esta tabla se irá actualizando a medida que se agreguen nuevas funcionalidades o permisos a cada perfil.

## 💰 Historial de Precios de Compra

### Funcionalidad
El sistema ahora incluye un completo historial de precios de compra que permite:

- **Registro obligatorio de precios** en cada recepción de compra
- **Estadísticas de precios** por elemento (promedio, mínimo, máximo, último)
- **Vista detallada** del historial completo de recepciones
- **Información en reportes** con precios promedio y último precio
- **Acceso rápido** desde la lista de elementos (rol Comprador)

### Características
- **Campo obligatorio:** El precio unitario es requerido en todas las recepciones
- **Validación:** Solo acepta valores mayores a cero
- **Estadísticas automáticas:** Cálculo de precios promedio, mínimo y máximo
- **Interfaz intuitiva:** Botón de acceso directo en la lista de elementos
- **Reportes mejorados:** Incluye información de precios en los reportes generales

### Acceso
- **Rol Comprador:** Acceso completo al historial de precios
- **Rol Gestor:** Puede ver precios en reportes
- **Rol Gerente de Proyectos:** Puede ver precios en reportes

### Uso
1. **Registrar compra:** Al crear una recepción, el precio unitario es obligatorio
2. **Ver historial:** Hacer clic en el ícono de gráfico en la lista de elementos
3. **Analizar precios:** Revisar estadísticas y tendencias de precios
4. **Reportes:** Consultar precios en el módulo de reportes
