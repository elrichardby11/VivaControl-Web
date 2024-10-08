# Generated by Django 5.0.6 on 2024-08-22 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrador', '0001_initial'),
        ('auxiliares', '0001_initial'),
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CStateMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PagoMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_pago', models.IntegerField()),
                ('monto', models.IntegerField()),
                ('metodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.metodospago')),
            ],
            options={
                'unique_together': {('id_pago', 'metodo')},
            },
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('periodo', models.IntegerField()),
                ('precio_total', models.IntegerField(blank=True, null=True)),
                ('coste_total', models.IntegerField()),
                ('auxiliar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auxiliares.auxiliar')),
                ('cstate_movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.cstatemovimiento')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.pagomovimiento')),
                ('tipo_movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.tipomovimiento')),
            ],
        ),
        migrations.CreateModel(
            name='SucursalProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
                ('id_sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.sucursal')),
            ],
            options={
                'unique_together': {('id_sucursal', 'id_producto')},
            },
        ),
        migrations.CreateModel(
            name='DetalleMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.IntegerField()),
                ('coste_unitario', models.IntegerField()),
                ('movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.movimiento')),
                ('sucursal_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.sucursalproducto')),
            ],
            options={
                'unique_together': {('movimiento', 'sucursal_producto')},
            },
        ),
    ]
