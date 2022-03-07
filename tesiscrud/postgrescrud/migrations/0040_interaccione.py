# Generated by Django 4.0.2 on 2022-03-06 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postgrescrud', '0039_alter_interacciones_cedula'),
    ]

    operations = [
        migrations.CreateModel(
            name='interaccione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('razon', models.CharField(max_length=20)),
                ('cedula', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cedul', to='postgrescrud.usuarios')),
            ],
            options={
                'verbose_name_plural': 'Interacciones',
            },
        ),
    ]
