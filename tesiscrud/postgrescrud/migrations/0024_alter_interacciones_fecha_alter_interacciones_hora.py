# Generated by Django 4.0.2 on 2022-03-05 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postgrescrud', '0023_alter_interacciones_fecha_alter_interacciones_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interacciones',
            name='fecha',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='interacciones',
            name='hora',
            field=models.TimeField(),
        ),
    ]
