# Generated by Django 4.0.2 on 2022-03-05 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postgrescrud', '0012_contratos_oficina_contrato'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contratos',
            old_name='contrato',
            new_name='nombre',
        ),
    ]
