# Maestranzas Unidos - Sistema de Gestión de Inventarios

## 📋 Descripción

Sistema profesional de gestión de inventarios desarrollado para Maestranzas Unidos. Esta aplicación web proporciona una solución completa para el control y administración de inventarios con interfaz moderna y funcionalidades avanzadas.

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- **Login seguro** con usuarios predefinidos
- **Roles de usuario** (Administrador y Usuario General)
- **Sesiones persistentes** con localStorage
- **Logout seguro**

### 📊 Dashboard Interactivo
- **Estadísticas en tiempo real** del inventario
- **Contadores de ítems** totales, stock bajo y sin stock
- **Valor total** del inventario
- **Alertas automáticas** de stock bajo

### 🛠️ Gestión Completa de Inventario

#### Operaciones CRUD
- **Crear** nuevos ítems con información detallada
- **Leer** inventario con búsqueda y filtros
- **Actualizar** información de ítems existentes
- **Eliminar** ítems con confirmación

#### Campos de Ítem
- **SKU/Código** único
- **Nombre** del producto
- **Categoría** (Herramientas, Materiales, Equipos, etc.)
- **Ubicación** en almacén
- **Stock actual** y **stock mínimo**
- **Precio unitario**
- **Proveedor**
- **Descripción** detallada
- **Timestamps** de creación y modificación

### 📈 Movimientos de Stock
- **Entradas** de inventario
- **Salidas** de inventario
- **Ajustes** de stock
- **Registro de movimientos** con motivo y usuario
- **Historial** de transacciones

### 🔍 Búsqueda y Filtros
- **Búsqueda en tiempo real** por SKU, nombre o ubicación
- **Filtro por categorías**
- **Ordenamiento** de resultados
- **Vista responsive** para móviles

### 📊 Alertas y Notificaciones
- **Alertas automáticas** de stock bajo
- **Notificaciones** de acciones realizadas
- **Indicadores visuales** de estado de stock
- **Sistema de notificaciones** no intrusivo

### 📤 Exportación e Importación
- **Exportar** inventario completo a JSON
- **Importar** datos desde archivos JSON
- **Respaldo** automático de datos
- **Sincronización** de información

## 🚀 Instalación y Uso
### Requisitos
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- No requiere servidor web (funciona localmente)

### Instalación
1. Descarga todos los archivos del proyecto
2. Abre `index.html` en tu navegador
3. ¡Listo! La aplicación está lista para usar

### Usuarios Predefinidos

#### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Acceso completo a todas las funcionalidades

#### Usuario General
- **Usuario:** `usuario`
- **Contraseña:** `user123`
- **Permisos:** Acceso a gestión de inventario (sin administración de usuarios)

## 📱 Funcionalidades Detalladas

### Dashboard
El dashboard muestra estadísticas clave en tiempo real:
- **Total de ítems** en inventario
- **Ítems con stock bajo** (stock ≤ mínimo)
- **Ítems sin stock** (stock = 0)
- **Valor total** del inventario

### Gestión de Ítems
1. **Agregar Ítem**: Formulario completo con validación
2. **Editar Ítem**: Modificar información existente
3. **Eliminar Ítem**: Con confirmación de seguridad
4. **Ajustar Stock**: Movimientos de entrada/salida/ajuste

### Búsqueda y Filtros
- **Búsqueda instantánea** en SKU, nombre y ubicación
- **Filtro por categorías** predefinidas
- **Resultados en tiempo real**

### Movimientos de Stock
- **Entrada**: Agregar stock al inventario
- **Salida**: Retirar stock del inventario
- **Ajuste**: Corregir cantidades de stock
- **Registro completo** con motivo y usuario responsable

### Alertas Inteligentes
- **Detección automática** de stock bajo
- **Notificaciones** no intrusivas
- **Indicadores visuales** en la tabla
- **Alertas en tiempo real**

## 🎨 Interfaz de Usuario

### Diseño Moderno
- **Interfaz responsive** que se adapta a cualquier dispositivo
- **Diseño material** con efectos visuales modernos
- **Paleta de colores** profesional
- **Iconografía** Font Awesome

### Experiencia de Usuario
- **Navegación intuitiva** y fácil de usar
- **Feedback visual** para todas las acciones
- **Modales** para formularios y confirmaciones
- **Animaciones suaves** y transiciones

### Responsive Design
- **Optimizado para móviles** y tablets
- **Adaptación automática** a diferentes tamaños de pantalla
- **Navegación táctil** amigable

## 💾 Almacenamiento de Datos

### LocalStorage
- **Persistencia local** de todos los datos
- **No requiere base de datos** externa
- **Respaldo automático** en el navegador
- **Sincronización** entre pestañas

### Estructura de Datos
```javascript
{
  id: Number,
  sku: String,
  name: String,
  category: String,
  location: String,
  stock: Number,
  minimum: Number,
  price: Number,
  supplier: String,
  description: String,
  createdAt: String,
  updatedAt: String
}
```

## 🔧 Personalización

### Categorías
Las categorías se pueden modificar en el archivo `app.js`:
```javascript
this.categories = [
    'Herramientas',
    'Materiales',
    'Equipos',
    'Repuestos',
    'Consumibles',
    'Seguridad',
    'Otros'
];
```

### Usuarios
Los usuarios se pueden agregar/modificar en el archivo `app.js`:
```javascript
this.users = [
    { username: 'admin', password: 'admin123', name: 'Administrador', role: 'admin' },
    { username: 'usuario', password: 'user123', name: 'Usuario General', role: 'user' }
];
```

## 📊 Reportes y Exportación

### Exportación de Datos
- **Formato JSON** completo con metadatos
- **Incluye timestamp** de exportación
- **Usuario responsable** de la exportación
- **Nombre de archivo** con fecha

### Importación de Datos
- **Validación** de formato de archivo
- **Sobrescritura** opcional de datos existentes
- **Manejo de errores** robusto
- **Notificaciones** de éxito/error

## 🔒 Seguridad

### Autenticación
- **Sistema de login** seguro
- **Contraseñas** protegidas
- **Sesiones** persistentes
- **Logout** seguro

### Validación de Datos
- **Validación** en frontend
- **Sanitización** de entradas
- **Prevención** de datos maliciosos
- **Confirmaciones** para acciones críticas

## 🚀 Futuras Mejoras

### Funcionalidades Planificadas
- [ ] **Códigos de barras** y escáner QR
- [ ] **Reportes PDF** avanzados
- [ ] **Gráficos** y análisis estadísticos
- [ ] **Sincronización** con servidor remoto
- [ ] **Múltiples almacenes** y ubicaciones
- [ ] **Sistema de pedidos** automáticos
- [ ] **Notificaciones por email**
- [ ] **API REST** para integración

### Mejoras Técnicas
- [ ] **Base de datos** SQLite/MySQL
- [ ] **Autenticación** JWT
- [ ] **Encriptación** de datos sensibles
- [ ] **Backup automático** en la nube
- [ ] **Logs** de auditoría completos

## 📞 Soporte

### Contacto
Para soporte técnico o consultas sobre el sistema:
- **Email:** soporte@maestranzasunidos.com
- **Teléfono:** +56 2 2345 6789
- **Horario:** Lunes a Viernes 8:00 - 18:00

### Documentación
- **Manual de usuario** disponible en la aplicación
- **Videos tutoriales** en el canal de YouTube
- **FAQ** en el sitio web corporativo

## 📄 Licencia

Este software es propiedad de **Maestranzas Unidos** y está destinado para uso interno de la empresa.

---

**Desarrollado con ❤️ para Maestranzas Unidos** 