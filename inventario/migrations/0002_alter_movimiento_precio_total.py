# Generated by Django 5.0.6 on 2024-07-05 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='precio_total',
            field=models.IntegerField(blank=True),
        ),
    ]