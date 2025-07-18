# Generated by Django 5.2.3 on 2025-07-02 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0010_alter_asignacionrecurso_cantidad_disponible'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('status', models.CharField(choices=[('PENDING', 'Pendiente'), ('RECEIVED', 'Recibido')], default='PENDING', max_length=10, verbose_name='Estado')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.proveedor', verbose_name='Proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('elemento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.elementoinventario', verbose_name='Ítem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='inventario.purchaseorder', verbose_name='Orden')),
            ],
        ),
    ]
