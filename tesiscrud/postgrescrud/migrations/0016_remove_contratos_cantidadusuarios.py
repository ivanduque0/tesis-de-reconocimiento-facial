# Generated by Django 4.0.2 on 2022-03-05 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postgrescrud', '0015_contratos_cantidadusuarios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contratos',
            name='cantidadusuarios',
        ),
    ]
