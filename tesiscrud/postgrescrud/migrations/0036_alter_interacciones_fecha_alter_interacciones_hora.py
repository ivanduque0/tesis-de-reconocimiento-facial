# Generated by Django 4.0.2 on 2022-03-06 00:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postgrescrud', '0035_alter_contratos_nombre_alter_usuarios_contrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interacciones',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='interacciones',
            name='hora',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
