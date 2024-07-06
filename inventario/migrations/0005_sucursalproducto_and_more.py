# Generated by Django 5.0.6 on 2024-07-06 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0001_initial'),
        ('inventario', '0004_alter_detallemovimiento_unique_together_and_more'),
        ('productos', '0001_initial'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='detallemovimiento',
            name='sucursal_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.sucursalproducto'),
        ),
    ]
