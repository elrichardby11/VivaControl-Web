# Generated by Django 5.0.6 on 2024-08-23 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0001_initial'),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagomovimiento',
            name='metodo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='administrador.metodospago'),
        ),
    ]