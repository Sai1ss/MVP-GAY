// =======================================================================
// CONFIGURACIÓN - MAESTRANZAS UNIDOS
// =======================================================================

const CONFIG = {
    // Información de la empresa
    COMPANY: {
        name: 'Maestranzas Unidos',
        logo: 'fas fa-tools',
        website: 'https://maestranzasunidos.com',
        email: 'contacto@maestranzasunidos.com',
        phone: '+56 2 2345 6789',
        address: 'Av. Principal 123, Santiago, Chile'
    },

    // Configuración de la aplicación
    APP: {
        title: 'Sistema de Gestión de Inventarios',
        version: '1.0.0',
        theme: {
            primary: '#667eea',
            secondary: '#764ba2',
            success: '#38a169',
            warning: '#ed8936',
            danger: '#e53e3e',
            info: '#3182ce'
        },
        autoSave: true,
        autoSaveInterval: 30000, // 30 segundos
        maxNotifications: 5,
        notificationTimeout: 5000 // 5 segundos
    },

    // Categorías de inventario
    CATEGORIES: [
        'Herramientas',
        'Materiales',
        'Equipos',
        'Repuestos',
        'Consumibles',
        'Seguridad',
        'Otros'
    ],

    // Usuarios del sistema
    USERS: [
        {
            username: 'admin',
            password: 'admin123',
            name: 'Administrador',
            role: 'admin',
            email: 'admin@maestranzasunidos.com'
        },
        {
            username: 'usuario',
            password: 'user123',
            name: 'Usuario General',
            role: 'user',
            email: 'usuario@maestranzasunidos.com'
        },
        {
            username: 'almacen',
            password: 'almacen123',
            name: 'Encargado de Almacén',
            role: 'user',
            email: 'almacen@maestranzasunidos.com'
        }
    ],

    // Configuración de stock
    STOCK: {
        defaultMinimum: 0,
        defaultPrice: 0,
        allowNegativeStock: false,
        lowStockThreshold: 0.2, // 20% del stock mínimo
        criticalStockThreshold: 0.1 // 10% del stock mínimo
    },

    // Configuración de exportación
    EXPORT: {
        defaultFormat: 'json',
        includeMetadata: true,
        includeMovements: true,
        filenamePrefix: 'inventario_maestranzas',
        dateFormat: 'YYYY-MM-DD'
    },

    // Configuración de notificaciones
    NOTIFICATIONS: {
        enableSound: false,
        enableDesktop: false,
        lowStockAlerts: true,
        outOfStockAlerts: true,
        movementAlerts: true
    },

    // Configuración de búsqueda
    SEARCH: {
        minCharacters: 2,
        searchDelay: 300, // milisegundos
        searchFields: ['sku', 'name', 'location', 'supplier', 'description']
    },

    // Configuración de paginación
    PAGINATION: {
        itemsPerPage: 25,
        maxPages: 10,
        showPageNumbers: true
    },

    // Configuración de validación
    VALIDATION: {
        sku: {
            required: true,
            minLength: 3,
            maxLength: 20,
            pattern: /^[A-Z0-9\-_]+$/
        },
        name: {
            required: true,
            minLength: 2,
            maxLength: 100
        },
        stock: {
            min: 0,
            max: 999999
        },
        price: {
            min: 0,
            max: 999999.99,
            decimals: 2
        }
    },

    // Mensajes del sistema
    MESSAGES: {
        login: {
            success: '¡Bienvenido!',
            error: 'Usuario o contraseña incorrectos',
            logout: 'Has cerrado sesión correctamente'
        },
        inventory: {
            add: 'Ítem agregado exitosamente',
            update: 'Ítem actualizado exitosamente',
            delete: 'Ítem eliminado exitosamente',
            confirmDelete: '¿Estás seguro de que deseas eliminar este ítem?',
            stockLow: 'Stock bajo detectado',
            stockOut: 'Stock agotado'
        },
        movement: {
            success: 'Movimiento registrado exitosamente',
            error: 'Error al registrar movimiento'
        },
        export: {
            success: 'Datos exportados exitosamente',
            error: 'Error al exportar datos'
        },
        import: {
            success: 'Datos importados exitosamente',
            error: 'Error al importar datos',
            invalidFormat: 'Formato de archivo inválido'
        }
    },

    // Configuración de reportes
    REPORTS: {
        enablePDF: false,
        enableExcel: false,
        enableCharts: false,
        defaultPeriod: 'month',
        includeCharts: true,
        includeTables: true
    },

    // Configuración de seguridad
    SECURITY: {
        sessionTimeout: 3600000, // 1 hora
        maxLoginAttempts: 3,
        lockoutDuration: 900000, // 15 minutos
        requirePasswordChange: false,
        passwordMinLength: 6
    },

    // Configuración de backup
    BACKUP: {
        autoBackup: true,
        backupInterval: 86400000, // 24 horas
        maxBackups: 7,
        includeSettings: true
    },

    // Configuración de logs
    LOGGING: {
        enableLogs: true,
        logLevel: 'info', // debug, info, warn, error
        logRetention: 30, // días
        logUserActions: true,
        logSystemEvents: true
    }
};

// Exportar configuración para uso global
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
} 