# Generated by Django 4.0.2 on 2022-03-04 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postgrescrud', '0003_interacciones_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interacciones',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='interacciones',
            name='hora',
        ),
        migrations.RemoveField(
            model_name='interacciones',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='interacciones',
            name='razon',
        ),
    ]
