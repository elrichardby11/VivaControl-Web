# Generated by Django 5.0.6 on 2024-07-05 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auxiliares', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetodosPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=225)),
                ('descripcion', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id_sucursal', models.IntegerField(primary_key=True, serialize=False)),
                ('direccion', models.CharField(max_length=255)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auxiliares.comuna')),
            ],
        ),
    ]