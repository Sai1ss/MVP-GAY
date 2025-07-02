from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

# ===== NUEVOS MODELOS PARA CATEGORIZACIÓN =====
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Color en formato hexadecimal')
    
    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6c757d', help_text='Color en formato hexadecimal')
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class ElementoInventario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    numero_serie = models.CharField(max_length=50, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    ubicacion = models.CharField(max_length=100)
    lote = models.CharField(max_length=50, blank=True, null=True, help_text="Identificador de lote (opcional)")
    fecha_vencimiento = models.DateField(blank=True, null=True, help_text="Fecha de vencimiento (opcional)")
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"

class RecepcionCompra(models.Model):
    elemento = models.ForeignKey(ElementoInventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# Nuevos modelos para funcionalidades específicas de roles

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('transferencia', 'Transferencia'),
        ('devolucion', 'Devolución'),
        ('ajuste', 'Ajuste'),
        ('auditoria', 'Ajuste por Auditoría'),
    ]
    
    ORIGEN_CHOICES = [
        ('compra', 'Compra'),
        ('solicitud', 'Solicitud de Material'),
        ('devolucion', 'Devolución'),
        ('transferencia', 'Transferencia'),
        ('ajuste_manual', 'Ajuste Manual'),
        ('auditoria', 'Auditoría'),
        ('sistema', 'Sistema'),
    ]
    
    elemento = models.ForeignKey(ElementoInventario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default='sistema')
    cantidad = models.IntegerField()  # Positivo para entrada, negativo para salida
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    proyecto = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    
    # Campos para rastrear el origen específico
    recepcion_compra = models.ForeignKey('RecepcionCompra', on_delete=models.SET_NULL, null=True, blank=True)
    solicitud_material = models.ForeignKey('SolicitudMaterial', on_delete=models.SET_NULL, null=True, blank=True)
    auditoria_inventario = models.ForeignKey('AuditoriaInventario', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Stock antes y después del movimiento
    stock_anterior = models.PositiveIntegerField(null=True, blank=True)
    stock_nuevo = models.PositiveIntegerField(null=True, blank=True)
    
    eliminado = models.BooleanField(default=False)
    motivo_eliminacion = models.TextField(blank=True, null=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)
    usuario_eliminacion = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL, related_name='movimientos_eliminados')
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
    
    def save(self, *args, **kwargs):
        # Calcular stock anterior y nuevo
        if not self.pk:  # Solo para nuevos registros
            self.stock_anterior = self.elemento.stock_actual
            if self.tipo in ['entrada', 'devolucion']:
                self.stock_nuevo = self.stock_anterior + self.cantidad
            elif self.tipo in ['salida', 'transferencia']:
                self.stock_nuevo = self.stock_anterior - abs(self.cantidad)
            elif self.tipo == 'ajuste':
                self.stock_nuevo = self.stock_anterior + self.cantidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.elemento.nombre} ({self.cantidad:+d}) - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def descripcion_completa(self):
        """Retorna una descripción completa del movimiento"""
        desc = f"{self.get_tipo_display()} de {abs(self.cantidad)} unidades"
        if self.proyecto:
            desc += f" - Proyecto: {self.proyecto}"
        if self.observaciones:
            desc += f" - {self.observaciones}"
        return desc

class SolicitudMaterial(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('entregada', 'Entregada'),
    ]
    
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    elemento = models.ForeignKey(ElementoInventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    proyecto = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Solicitud {self.id} - {self.elemento.nombre}"

class AuditoriaInventario(models.Model):
    auditor = models.ForeignKey(User, on_delete=models.CASCADE)
    elemento = models.ForeignKey(ElementoInventario, on_delete=models.CASCADE)
    stock_sistema = models.PositiveIntegerField()
    stock_fisico = models.PositiveIntegerField()
    diferencia = models.IntegerField()
    fecha_auditoria = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.diferencia = self.stock_fisico - self.stock_sistema
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Auditoría {self.id} - {self.elemento.nombre}"

class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('planificacion', 'Planificación'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    gerente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificacion')
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

# ===== FUNCIONES HELPER PARA MOVIMIENTOS AUTÁTICOS =====

def crear_movimiento_automatico(elemento, tipo, cantidad, usuario, origen='sistema', 
                               proyecto='', observaciones='', recepcion_compra=None, 
                               solicitud_material=None, auditoria_inventario=None):
    """
    Función helper para crear movimientos de inventario automáticamente
    """
    # Asegurar que la cantidad sea positiva para entradas y negativa para salidas
    if tipo in ['entrada', 'devolucion'] and cantidad < 0:
        cantidad = abs(cantidad)
    elif tipo in ['salida', 'transferencia'] and cantidad > 0:
        cantidad = -abs(cantidad)
    
    # Crear el movimiento
    movimiento = MovimientoInventario.objects.create(
        elemento=elemento,
        tipo=tipo,
        origen=origen,
        cantidad=cantidad,
        usuario=usuario,
        proyecto=proyecto,
        observaciones=observaciones,
        recepcion_compra=recepcion_compra,
        solicitud_material=solicitud_material,
        auditoria_inventario=auditoria_inventario
    )
    
    # Actualizar el stock del elemento
    if tipo in ['entrada', 'devolucion']:
        elemento.stock_actual += abs(cantidad)
    elif tipo in ['salida', 'transferencia']:
        elemento.stock_actual -= abs(cantidad)
    elif tipo == 'ajuste':
        elemento.stock_actual += cantidad
    
    elemento.save()
    
    return movimiento

class ConfiguracionSistema(models.Model):
    """Modelo para almacenar configuraciones del sistema"""
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre de la configuración")
    valor = models.TextField(help_text="Valor de la configuración")
    descripcion = models.TextField(blank=True, help_text="Descripción de la configuración")
    categoria = models.CharField(max_length=50, choices=[
        ('inventario', 'Inventario'),
        ('alertas', 'Alertas'),
        ('seguridad', 'Seguridad'),
        ('general', 'General'),
    ], default='general')
    activo = models.BooleanField(default=True, help_text="Indica si la configuración está activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
    
    @classmethod
    def get_valor(cls, nombre, valor_por_defecto=None):
        """Obtener el valor de una configuración"""
        try:
            config = cls.objects.get(nombre=nombre, activo=True)
            return config.valor
        except cls.DoesNotExist:
            return valor_por_defecto
    
    @classmethod
    def set_valor(cls, nombre, valor, descripcion="", categoria="general", usuario=None):
        """Establecer el valor de una configuración"""
        config, created = cls.objects.get_or_create(
            nombre=nombre,
            defaults={
                'valor': str(valor),
                'descripcion': descripcion,
                'categoria': categoria,
                'modificado_por': usuario
            }
        )
        if not created:
            config.valor = str(valor)
            config.descripcion = descripcion
            config.categoria = categoria
            config.modificado_por = usuario
            config.save()
        return config

class AsignacionRecurso(models.Model):
    ESTADOS = [
        ('reservado', 'Reservado'),
        ('en_uso', 'En Uso'),
        ('liberado', 'Liberado'),
        ('cancelado', 'Cancelado'),
    ]
    
    elemento = models.ForeignKey(ElementoInventario, on_delete=models.CASCADE, related_name='asignaciones')
    proyecto = models.CharField(max_length=200)
    cantidad_asignada = models.PositiveIntegerField()
    cantidad_disponible = models.PositiveIntegerField(default=0)  # Cantidad que aún no se ha usado
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_liberacion_estimada = models.DateField()
    fecha_liberacion_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='reservado')
    asignado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignaciones_creadas')
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_asignacion']
        verbose_name = 'Asignación de Recurso'
        verbose_name_plural = 'Asignaciones de Recursos'
    
    def __str__(self):
        return f"{self.elemento.nombre} - {self.proyecto} ({self.cantidad_asignada})"
    
    def save(self, *args, **kwargs):
        # Si es una nueva asignación, verificar disponibilidad
        if not self.pk:
            stock_disponible = self.elemento.stock_actual
            asignaciones_activas = AsignacionRecurso.objects.filter(
                elemento=self.elemento,
                estado__in=['reservado', 'en_uso']
            ).exclude(pk=self.pk)
            
            stock_reservado = sum(a.cantidad_asignada for a in asignaciones_activas)
            stock_realmente_disponible = stock_disponible - stock_reservado
            
            if self.cantidad_asignada > stock_realmente_disponible:
                raise ValueError(f"No hay suficiente stock disponible. Disponible: {stock_realmente_disponible}")
        
        super().save(*args, **kwargs)
    
    @property
    def porcentaje_uso(self):
        """Calcula el porcentaje de uso del recurso asignado"""
        if self.cantidad_asignada == 0:
            return 0
        usado = self.cantidad_asignada - self.cantidad_disponible
        return (usado / self.cantidad_asignada) * 100
    
    def liberar(self, usuario):
        """Libera la asignación y actualiza el estado"""
        self.estado = 'liberado'
        self.fecha_liberacion_real = date.today()
        self.save()
        
        # Crear movimiento automático de liberación
        crear_movimiento_automatico(
            elemento=self.elemento,
            tipo='entrada',
            cantidad=self.cantidad_disponible,
            usuario=usuario,
            proyecto=self.proyecto,
            observaciones=f'Liberación de asignación - {self.cantidad_disponible} unidades devueltas'
        )
    
    def cancelar(self, usuario):
        """Cancela la asignación"""
        self.estado = 'cancelado'
        self.fecha_liberacion_real = date.today()
        self.save()
        
        # Crear movimiento automático de cancelación
        crear_movimiento_automatico(
            elemento=self.elemento,
            tipo='entrada',
            cantidad=self.cantidad_disponible,
            usuario=usuario,
            proyecto=self.proyecto,
            observaciones=f'Cancelación de asignación - {self.cantidad_disponible} unidades devueltas'
        )


